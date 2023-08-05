# orm/events.py
# Copyright (C) 2005-2023 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""ORM event interfaces.

"""
from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Collection
from typing import Dict
from typing import Generic
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union
import weakref

from . import instrumentation
from . import interfaces
from . import mapperlib
from .attributes import QueryableAttribute
from .base import _mapper_or_none
from .base import NO_KEY
from .instrumentation import ClassManager
from .instrumentation import InstrumentationFactory
from .query import BulkDelete
from .query import BulkUpdate
from .query import Query
from .scoping import scoped_session
from .session import Session
from .session import sessionmaker
from .. import event
from .. import exc
from .. import util
from ..event import EventTarget
from ..event.registry import _ET
from ..util.compat import inspect_getfullargspec

if TYPE_CHECKING:
    from weakref import ReferenceType

    from ._typing import _InstanceDict
    from ._typing import _InternalEntityType
    from ._typing import _O
    from ._typing import _T
    from .attributes import Event
    from .base import EventConstants
    from .session import ORMExecuteState
    from .session import SessionTransaction
    from .unitofwork import UOWTransaction
    from ..engine import Connection
    from ..event.base import _Dispatch
    from ..event.base import _HasEventsDispatch
    from ..event.registry import _EventKey
    from ..orm.collections import CollectionAdapter
    from ..orm.context import QueryContext
    from ..orm.decl_api import DeclarativeAttributeIntercept
    from ..orm.decl_api import DeclarativeMeta
    from ..orm.mapper import Mapper
    from ..orm.state import InstanceState

_KT = TypeVar("_KT", bound=Any)
_ET2 = TypeVar("_ET2", bound=EventTarget)


class InstrumentationEvents(event.Events[InstrumentationFactory]):
    """Events related to class instrumentation events.

    The listeners here support being established against
    any new style class, that is any object that is a subclass
    of 'type'.  Events will then be fired off for events
    against that class.  If the "propagate=True" flag is passed
    to event.listen(), the event will fire off for subclasses
    of that class as well.

    The Python ``type`` builtin is also accepted as a target,
    which when used has the effect of events being emitted
    for all classes.

    Note the "propagate" flag here is defaulted to ``True``,
    unlike the other class level events where it defaults
    to ``False``.  This means that new subclasses will also
    be the subject of these events, when a listener
    is established on a superclass.

    """

    _target_class_doc = "SomeBaseClass"
    _dispatch_target = InstrumentationFactory

    @classmethod
    def _accept_with(
        cls,
        target: Union[
            InstrumentationFactory,
            Type[InstrumentationFactory],
        ],
        identifier: str,
    ) -> Optional[
        Union[
            InstrumentationFactory,
            Type[InstrumentationFactory],
        ]
    ]:
        if isinstance(target, type):
            return _InstrumentationEventsHold(target)  # type: ignore [return-value] # noqa: E501
        else:
            return None

    @classmethod
    def _listen(
        cls, event_key: _EventKey[_T], propagate: bool = True, **kw: Any
    ) -> None:
        target, identifier, fn = (
            event_key.dispatch_target,
            event_key.identifier,
            event_key._listen_fn,
        )

        def listen(target_cls: type, *arg: Any) -> Optional[Any]:
            listen_cls = target()

            # if weakref were collected, however this is not something
            # that normally happens.   it was occurring during test teardown
            # between mapper/registry/instrumentation_manager, however this
            # interaction was changed to not rely upon the event system.
            if listen_cls is None:
                return None

            if propagate and issubclass(target_cls, listen_cls):
                return fn(target_cls, *arg)
            elif not propagate and target_cls is listen_cls:
                return fn(target_cls, *arg)
            else:
                return None

        def remove(ref: ReferenceType[_T]) -> None:
            key = event.registry._EventKey(  # type: ignore [type-var]
                None,
                identifier,
                listen,
                instrumentation._instrumentation_factory,
            )
            getattr(
                instrumentation._instrumentation_factory.dispatch, identifier
            ).remove(key)

        target = weakref.ref(target.class_, remove)

        event_key.with_dispatch_target(
            instrumentation._instrumentation_factory
        ).with_wrapper(listen).base_listen(**kw)

    @classmethod
    def _clear(cls) -> None:
        super()._clear()
        instrumentation._instrumentation_factory.dispatch._clear()

    def class_instrument(self, cls: ClassManager[_O]) -> None:
        """Called after the given class is instrumented.

        To get at the :class:`.ClassManager`, use
        :func:`.manager_of_class`.

        """

    def class_uninstrument(self, cls: ClassManager[_O]) -> None:
        """Called before the given class is uninstrumented.

        To get at the :class:`.ClassManager`, use
        :func:`.manager_of_class`.

        """

    def attribute_instrument(
        self, cls: ClassManager[_O], key: _KT, inst: _O
    ) -> None:
        """Called when an attribute is instrumented."""


class _InstrumentationEventsHold:
    """temporary marker object used to transfer from _accept_with() to
    _listen() on the InstrumentationEvents class.

    """

    def __init__(self, class_: type) -> None:
        self.class_ = class_

    dispatch = event.dispatcher(InstrumentationEvents)


class InstanceEvents(event.Events[ClassManager[Any]]):
    """Define events specific to object lifecycle.

    e.g.::

        from sqlalchemy import event

        def my_load_listener(target, context):
            print("on load!")

        event.listen(SomeClass, 'load', my_load_listener)

    Available targets include:

    * mapped classes
    * unmapped superclasses of mapped or to-be-mapped classes
      (using the ``propagate=True`` flag)
    * :class:`_orm.Mapper` objects
    * the :class:`_orm.Mapper` class itself indicates listening for all
      mappers.

    Instance events are closely related to mapper events, but
    are more specific to the instance and its instrumentation,
    rather than its system of persistence.

    When using :class:`.InstanceEvents`, several modifiers are
    available to the :func:`.event.listen` function.

    :param propagate=False: When True, the event listener should
       be applied to all inheriting classes as well as the
       class which is the target of this listener.
    :param raw=False: When True, the "target" argument passed
       to applicable event listener functions will be the
       instance's :class:`.InstanceState` management
       object, rather than the mapped instance itself.
    :param restore_load_context=False: Applies to the
       :meth:`.InstanceEvents.load` and :meth:`.InstanceEvents.refresh`
       events.  Restores the loader context of the object when the event
       hook is complete, so that ongoing eager load operations continue
       to target the object appropriately.  A warning is emitted if the
       object is moved to a new loader context from within one of these
       events if this flag is not set.

       .. versionadded:: 1.3.14


    """

    _target_class_doc = "SomeClass"

    _dispatch_target = ClassManager

    @classmethod
    def _new_classmanager_instance(
        cls,
        class_: Union[DeclarativeAttributeIntercept, DeclarativeMeta, type],
        classmanager: ClassManager[_O],
    ) -> None:
        _InstanceEventsHold.populate(class_, classmanager)

    @classmethod
    @util.preload_module("sqlalchemy.orm")
    def _accept_with(
        cls,
        target: Union[
            ClassManager[Any],
            Type[ClassManager[Any]],
        ],
        identifier: str,
    ) -> Optional[Union[ClassManager[Any], Type[ClassManager[Any]]]]:
        orm = util.preloaded.orm

        if isinstance(target, ClassManager):
            return target
        elif isinstance(target, mapperlib.Mapper):
            return target.class_manager
        elif target is orm.mapper:  # type: ignore [attr-defined]
            util.warn_deprecated(
                "The `sqlalchemy.orm.mapper()` symbol is deprecated and "
                "will be removed in a future release. For the mapper-wide "
                "event target, use the 'sqlalchemy.orm.Mapper' class.",
                "2.0",
            )
            return ClassManager
        elif isinstance(target, type):
            if issubclass(target, mapperlib.Mapper):
                return ClassManager
            else:
                manager = instrumentation.opt_manager_of_class(target)
                if manager:
                    return manager
                else:
                    return _InstanceEventsHold(target)  # type: ignore [return-value] # noqa: E501
        return None

    @classmethod
    def _listen(
        cls,
        event_key: _EventKey[ClassManager[Any]],
        raw: bool = False,
        propagate: bool = False,
        restore_load_context: bool = False,
        **kw: Any,
    ) -> None:
        target, fn = (event_key.dispatch_target, event_key._listen_fn)

        if not raw or restore_load_context:

            def wrap(
                state: InstanceState[_O], *arg: Any, **kw: Any
            ) -> Optional[Any]:
                if not raw:
                    target: Any = state.obj()
                else:
                    target = state
                if restore_load_context:
                    runid = state.runid
                try:
                    return fn(target, *arg, **kw)
                finally:
                    if restore_load_context:
                        state.runid = runid

            event_key = event_key.with_wrapper(wrap)

        event_key.base_listen(propagate=propagate, **kw)

        if propagate:
            for mgr in target.subclass_managers(True):
                event_key.with_dispatch_target(mgr).base_listen(propagate=True)

    @classmethod
    def _clear(cls) -> None:
        super()._clear()
        _InstanceEventsHold._clear()

    def first_init(self, manager: ClassManager[_O], cls: Type[_O]) -> None:
        """Called when the first instance of a particular mapping is called.

        This event is called when the ``__init__`` method of a class
        is called the first time for that particular class.    The event
        invokes before ``__init__`` actually proceeds as well as before
        the :meth:`.InstanceEvents.init` event is invoked.

        """

    def init(self, target: _O, args: Any, kwargs: Any) -> None:
        """Receive an instance when its constructor is called.

        This method is only called during a userland construction of
        an object, in conjunction with the object's constructor, e.g.
        its ``__init__`` method.  It is not called when an object is
        loaded from the database; see the :meth:`.InstanceEvents.load`
        event in order to intercept a database load.

        The event is called before the actual ``__init__`` constructor
        of the object is called.  The ``kwargs`` dictionary may be
        modified in-place in order to affect what is passed to
        ``__init__``.

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param args: positional arguments passed to the ``__init__`` method.
         This is passed as a tuple and is currently immutable.
        :param kwargs: keyword arguments passed to the ``__init__`` method.
         This structure *can* be altered in place.

        .. seealso::

            :meth:`.InstanceEvents.init_failure`

            :meth:`.InstanceEvents.load`

        """

    def init_failure(self, target: _O, args: Any, kwargs: Any) -> None:
        """Receive an instance when its constructor has been called,
        and raised an exception.

        This method is only called during a userland construction of
        an object, in conjunction with the object's constructor, e.g.
        its ``__init__`` method. It is not called when an object is loaded
        from the database.

        The event is invoked after an exception raised by the ``__init__``
        method is caught.  After the event
        is invoked, the original exception is re-raised outwards, so that
        the construction of the object still raises an exception.   The
        actual exception and stack trace raised should be present in
        ``sys.exc_info()``.

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param args: positional arguments that were passed to the ``__init__``
         method.
        :param kwargs: keyword arguments that were passed to the ``__init__``
         method.

        .. seealso::

            :meth:`.InstanceEvents.init`

            :meth:`.InstanceEvents.load`

        """

    def _sa_event_merge_wo_load(
        self, target: _O, context: QueryContext
    ) -> None:
        """receive an object instance after it was the subject of a merge()
        call, when load=False was passed.

        The target would be the already-loaded object in the Session which
        would have had its attributes overwritten by the incoming object. This
        overwrite operation does not use attribute events, instead just
        populating dict directly. Therefore the purpose of this event is so
        that extensions like sqlalchemy.ext.mutable know that object state has
        changed and incoming state needs to be set up for "parents" etc.

        This functionality is acceptable to be made public in a later release.

        .. versionadded:: 1.4.41

        """

    def load(self, target: _O, context: QueryContext) -> None:
        """Receive an object instance after it has been created via
        ``__new__``, and after initial attribute population has
        occurred.

        This typically occurs when the instance is created based on
        incoming result rows, and is only called once for that
        instance's lifetime.

        .. warning::

            During a result-row load, this event is invoked when the
            first row received for this instance is processed.  When using
            eager loading with collection-oriented attributes, the additional
            rows that are to be loaded / processed in order to load subsequent
            collection items have not occurred yet.   This has the effect
            both that collections will not be fully loaded, as well as that
            if an operation occurs within this event handler that emits
            another database load operation for the object, the "loading
            context" for the object can change and interfere with the
            existing eager loaders still in progress.

            Examples of what can cause the "loading context" to change within
            the event handler include, but are not necessarily limited to:

            * accessing deferred attributes that weren't part of the row,
              will trigger an "undefer" operation and refresh the object

            * accessing attributes on a joined-inheritance subclass that
              weren't part of the row, will trigger a refresh operation.

            As of SQLAlchemy 1.3.14, a warning is emitted when this occurs. The
            :paramref:`.InstanceEvents.restore_load_context` option may  be
            used on the event to prevent this warning; this will ensure that
            the existing loading context is maintained for the object after the
            event is called::

                @event.listens_for(
                    SomeClass, "load", restore_load_context=True)
                def on_load(instance, context):
                    instance.some_unloaded_attribute

            .. versionchanged:: 1.3.14 Added
               :paramref:`.InstanceEvents.restore_load_context`
               and :paramref:`.SessionEvents.restore_load_context` flags which
               apply to "on load" events, which will ensure that the loading
               context for an object is restored when the event hook is
               complete; a warning is emitted if the load context of the object
               changes without this flag being set.


        The :meth:`.InstanceEvents.load` event is also available in a
        class-method decorator format called :func:`_orm.reconstructor`.

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param context: the :class:`.QueryContext` corresponding to the
         current :class:`_query.Query` in progress.  This argument may be
         ``None`` if the load does not correspond to a :class:`_query.Query`,
         such as during :meth:`.Session.merge`.

        .. seealso::

            :meth:`.InstanceEvents.init`

            :meth:`.InstanceEvents.refresh`

            :meth:`.SessionEvents.loaded_as_persistent`

            :ref:`mapping_constructors`

        """

    def refresh(
        self, target: _O, context: QueryContext, attrs: Optional[Iterable[str]]
    ) -> None:
        """Receive an object instance after one or more attributes have
        been refreshed from a query.

        Contrast this to the :meth:`.InstanceEvents.load` method, which
        is invoked when the object is first loaded from a query.

        .. note:: This event is invoked within the loader process before
           eager loaders may have been completed, and the object's state may
           not be complete.  Additionally, invoking row-level refresh
           operations on the object will place the object into a new loader
           context, interfering with the existing load context.   See the note
           on :meth:`.InstanceEvents.load` for background on making use of the
           :paramref:`.InstanceEvents.restore_load_context` parameter, in
           order to resolve this scenario.

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param context: the :class:`.QueryContext` corresponding to the
         current :class:`_query.Query` in progress.
        :param attrs: sequence of attribute names which
         were populated, or None if all column-mapped, non-deferred
         attributes were populated.

        .. seealso::

            :meth:`.InstanceEvents.load`

        """

    def refresh_flush(
        self,
        target: _O,
        flush_context: UOWTransaction,
        attrs: Optional[Iterable[str]],
    ) -> None:
        """Receive an object instance after one or more attributes that
        contain a column-level default or onupdate handler have been refreshed
        during persistence of the object's state.

        This event is the same as :meth:`.InstanceEvents.refresh` except
        it is invoked within the unit of work flush process, and includes
        only non-primary-key columns that have column level default or
        onupdate handlers, including Python callables as well as server side
        defaults and triggers which may be fetched via the RETURNING clause.

        .. note::

            While the :meth:`.InstanceEvents.refresh_flush` event is triggered
            for an object that was INSERTed as well as for an object that was
            UPDATEd, the event is geared primarily  towards the UPDATE process;
            it is mostly an internal artifact that INSERT actions can also
            trigger this event, and note that **primary key columns for an
            INSERTed row are explicitly omitted** from this event.  In order to
            intercept the newly INSERTed state of an object, the
            :meth:`.SessionEvents.pending_to_persistent` and
            :meth:`.MapperEvents.after_insert` are better choices.

        .. versionadded:: 1.0.5

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param flush_context: Internal :class:`.UOWTransaction` object
         which handles the details of the flush.
        :param attrs: sequence of attribute names which
         were populated.

        .. seealso::

            :ref:`orm_server_defaults`

            :ref:`metadata_defaults_toplevel`

        """

    def expire(self, target: _O, attrs: Optional[Iterable[str]]) -> None:
        """Receive an object instance after its attributes or some subset
        have been expired.

        'keys' is a list of attribute names.  If None, the entire
        state was expired.

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param attrs: sequence of attribute
         names which were expired, or None if all attributes were
         expired.

        """

    def pickle(self, target: _O, state_dict: _InstanceDict) -> None:
        """Receive an object instance when its associated state is
        being pickled.

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param state_dict: the dictionary returned by
         :class:`.InstanceState.__getstate__`, containing the state
         to be pickled.

        """

    def unpickle(self, target: _O, state_dict: _InstanceDict) -> None:
        """Receive an object instance after its associated state has
        been unpickled.

        :param target: the mapped instance.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :param state_dict: the dictionary sent to
         :class:`.InstanceState.__setstate__`, containing the state
         dictionary which was pickled.

        """


class _EventsHold(event.RefCollection[_ET]):
    """Hold onto listeners against unmapped, uninstrumented classes.

    Establish _listen() for that class' mapper/instrumentation when
    those objects are created for that class.

    """

    all_holds: weakref.WeakKeyDictionary[Any, Any]

    def __init__(
        self,
        class_: Union[DeclarativeAttributeIntercept, DeclarativeMeta, type],
    ) -> None:
        self.class_ = class_

    @classmethod
    def _clear(cls) -> None:
        cls.all_holds.clear()

    class HoldEvents(Generic[_ET2]):
        _dispatch_target: Optional[Type[_ET2]] = None

        @classmethod
        def _listen(
            cls,
            event_key: _EventKey[_ET2],
            raw: bool = False,
            propagate: bool = False,
            retval: bool = False,
            **kw: Any,
        ) -> None:
            target = event_key.dispatch_target

            if target.class_ in target.all_holds:
                collection = target.all_holds[target.class_]
            else:
                collection = target.all_holds[target.class_] = {}

            event.registry._stored_in_collection(event_key, target)
            collection[event_key._key] = (
                event_key,
                raw,
                propagate,
                retval,
                kw,
            )

            if propagate:
                stack = list(target.class_.__subclasses__())
                while stack:
                    subclass = stack.pop(0)
                    stack.extend(subclass.__subclasses__())
                    subject = target.resolve(subclass)
                    if subject is not None:
                        # we are already going through __subclasses__()
                        # so leave generic propagate flag False
                        event_key.with_dispatch_target(subject).listen(
                            raw=raw, propagate=False, retval=retval, **kw
                        )

    def remove(self, event_key: _EventKey[_ET]) -> None:
        target = event_key.dispatch_target

        if isinstance(target, _EventsHold):
            collection = target.all_holds[target.class_]
            del collection[event_key._key]

    @classmethod
    def populate(
        cls,
        class_: Union[DeclarativeAttributeIntercept, DeclarativeMeta, type],
        subject: Union[ClassManager[_O], Mapper[_O]],
    ) -> None:
        for subclass in class_.__mro__:
            if subclass in cls.all_holds:
                collection = cls.all_holds[subclass]
                for (
                    event_key,
                    raw,
                    propagate,
                    retval,
                    kw,
                ) in collection.values():
                    if propagate or subclass is class_:
                        # since we can't be sure in what order different
                        # classes in a hierarchy are triggered with
                        # populate(), we rely upon _EventsHold for all event
                        # assignment, instead of using the generic propagate
                        # flag.
                        event_key.with_dispatch_target(subject).listen(
                            raw=raw, propagate=False, retval=retval, **kw
                        )


class _InstanceEventsHold(_EventsHold[_ET]):
    all_holds: weakref.WeakKeyDictionary[
        Any, Any
    ] = weakref.WeakKeyDictionary()

    def resolve(self, class_: Type[_O]) -> Optional[ClassManager[_O]]:
        return instrumentation.opt_manager_of_class(class_)

    class HoldInstanceEvents(_EventsHold.HoldEvents[_ET], InstanceEvents):  # type: ignore [misc] # noqa: E501
        pass

    dispatch = event.dispatcher(HoldInstanceEvents)


class MapperEvents(event.Events[mapperlib.Mapper[Any]]):
    """Define events specific to mappings.

    e.g.::

        from sqlalchemy import event

        def my_before_insert_listener(mapper, connection, target):
            # execute a stored procedure upon INSERT,
            # apply the value to the row to be inserted
            target.calculated_value = connection.execute(
                text("select my_special_function(%d)" % target.special_number)
            ).scalar()

        # associate the listener function with SomeClass,
        # to execute during the "before_insert" hook
        event.listen(
            SomeClass, 'before_insert', my_before_insert_listener)

    Available targets include:

    * mapped classes
    * unmapped superclasses of mapped or to-be-mapped classes
      (using the ``propagate=True`` flag)
    * :class:`_orm.Mapper` objects
    * the :class:`_orm.Mapper` class itself indicates listening for all
      mappers.

    Mapper events provide hooks into critical sections of the
    mapper, including those related to object instrumentation,
    object loading, and object persistence. In particular, the
    persistence methods :meth:`~.MapperEvents.before_insert`,
    and :meth:`~.MapperEvents.before_update` are popular
    places to augment the state being persisted - however, these
    methods operate with several significant restrictions. The
    user is encouraged to evaluate the
    :meth:`.SessionEvents.before_flush` and
    :meth:`.SessionEvents.after_flush` methods as more
    flexible and user-friendly hooks in which to apply
    additional database state during a flush.

    When using :class:`.MapperEvents`, several modifiers are
    available to the :func:`.event.listen` function.

    :param propagate=False: When True, the event listener should
       be applied to all inheriting mappers and/or the mappers of
       inheriting classes, as well as any
       mapper which is the target of this listener.
    :param raw=False: When True, the "target" argument passed
       to applicable event listener functions will be the
       instance's :class:`.InstanceState` management
       object, rather than the mapped instance itself.
    :param retval=False: when True, the user-defined event function
       must have a return value, the purpose of which is either to
       control subsequent event propagation, or to otherwise alter
       the operation in progress by the mapper.   Possible return
       values are:

       * ``sqlalchemy.orm.interfaces.EXT_CONTINUE`` - continue event
         processing normally.
       * ``sqlalchemy.orm.interfaces.EXT_STOP`` - cancel all subsequent
         event handlers in the chain.
       * other values - the return value specified by specific listeners.

    """

    _target_class_doc = "SomeClass"
    _dispatch_target = mapperlib.Mapper

    @classmethod
    def _new_mapper_instance(
        cls,
        class_: Union[DeclarativeAttributeIntercept, DeclarativeMeta, type],
        mapper: Mapper[_O],
    ) -> None:
        _MapperEventsHold.populate(class_, mapper)

    @classmethod
    @util.preload_module("sqlalchemy.orm")
    def _accept_with(
        cls,
        target: Union[mapperlib.Mapper[Any], Type[mapperlib.Mapper[Any]]],
        identifier: str,
    ) -> Optional[Union[mapperlib.Mapper[Any], Type[mapperlib.Mapper[Any]]]]:
        orm = util.preloaded.orm

        if target is orm.mapper:  # type: ignore [attr-defined]
            util.warn_deprecated(
                "The `sqlalchemy.orm.mapper()` symbol is deprecated and "
                "will be removed in a future release. For the mapper-wide "
                "event target, use the 'sqlalchemy.orm.Mapper' class.",
                "2.0",
            )
            return mapperlib.Mapper
        elif isinstance(target, type):
            if issubclass(target, mapperlib.Mapper):
                return target
            else:
                mapper = _mapper_or_none(target)
                if mapper is not None:
                    return mapper
                else:
                    return _MapperEventsHold(target)
        else:
            return target

    @classmethod
    def _listen(
        cls,
        event_key: _EventKey[_ET],
        raw: bool = False,
        retval: bool = False,
        propagate: bool = False,
        **kw: Any,
    ) -> None:
        target, identifier, fn = (
            event_key.dispatch_target,
            event_key.identifier,
            event_key._listen_fn,
        )

        if (
            identifier in ("before_configured", "after_configured")
            and target is not mapperlib.Mapper
        ):
            util.warn(
                "'before_configured' and 'after_configured' ORM events "
                "only invoke with the Mapper class "
                "as the target."
            )

        if not raw or not retval:
            if not raw:
                meth = getattr(cls, identifier)
                try:
                    target_index = (
                        inspect_getfullargspec(meth)[0].index("target") - 1
                    )
                except ValueError:
                    target_index = None

            def wrap(*arg: Any, **kw: Any) -> Any:
                if not raw and target_index is not None:
                    arg = list(arg)  # type: ignore [assignment]
                    arg[target_index] = arg[target_index].obj()  # type: ignore [index] # noqa: E501
                if not retval:
                    fn(*arg, **kw)
                    return interfaces.EXT_CONTINUE
                else:
                    return fn(*arg, **kw)

            event_key = event_key.with_wrapper(wrap)

        if propagate:
            for mapper in target.self_and_descendants:
                event_key.with_dispatch_target(mapper).base_listen(
                    propagate=True, **kw
                )
        else:
            event_key.base_listen(**kw)

    @classmethod
    def _clear(cls) -> None:
        super()._clear()
        _MapperEventsHold._clear()

    def instrument_class(self, mapper: Mapper[_O], class_: Type[_O]) -> None:
        r"""Receive a class when the mapper is first constructed,
        before instrumentation is applied to the mapped class.

        This event is the earliest phase of mapper construction.
        Most attributes of the mapper are not yet initialized.   To
        receive an event within initial mapper construction where basic
        state is available such as the :attr:`_orm.Mapper.attrs` collection,
        the :meth:`_orm.MapperEvents.after_mapper_constructed` event may
        be a better choice.

        This listener can either be applied to the :class:`_orm.Mapper`
        class overall, or to any un-mapped class which serves as a base
        for classes that will be mapped (using the ``propagate=True`` flag)::

            Base = declarative_base()

            @event.listens_for(Base, "instrument_class", propagate=True)
            def on_new_class(mapper, cls_):
                " ... "

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param class\_: the mapped class.

        .. seealso::

            :meth:`_orm.MapperEvents.after_mapper_constructed`

        """

    def after_mapper_constructed(
        self, mapper: Mapper[_O], class_: Type[_O]
    ) -> None:
        """Receive a class and mapper when the :class:`_orm.Mapper` has been
        fully constructed.

        This event is called after the initial constructor for
        :class:`_orm.Mapper` completes.  This occurs after the
        :meth:`_orm.MapperEvents.instrument_class` event and after the
        :class:`_orm.Mapper` has done an initial pass of its arguments
        to generate its collection of :class:`_orm.MapperProperty` objects,
        which are accessible via the :meth:`_orm.Mapper.get_property`
        method and the :attr:`_orm.Mapper.iterate_properties` attribute.

        This event differs from the
        :meth:`_orm.MapperEvents.before_mapper_configured` event in that it
        is invoked within the constructor for :class:`_orm.Mapper`, rather
        than within the :meth:`_orm.registry.configure` process.   Currently,
        this event is the only one which is appropriate for handlers that
        wish to create additional mapped classes in response to the
        construction of this :class:`_orm.Mapper`, which will be part of the
        same configure step when :meth:`_orm.registry.configure` next runs.

        .. versionadded:: 2.0.2

        .. seealso::

            :ref:`examples_versioning` - an example which illustrates the use
            of the :meth:`_orm.MapperEvents.before_mapper_configured`
            event to create new mappers to record change-audit histories on
            objects.

        """

    def before_mapper_configured(
        self, mapper: Mapper[_O], class_: Type[_O]
    ) -> None:
        """Called right before a specific mapper is to be configured.

        This event is intended to allow a specific mapper to be skipped during
        the configure step, by returning the :attr:`.orm.interfaces.EXT_SKIP`
        symbol which indicates to the :func:`.configure_mappers` call that this
        particular mapper (or hierarchy of mappers, if ``propagate=True`` is
        used) should be skipped in the current configuration run. When one or
        more mappers are skipped, the he "new mappers" flag will remain set,
        meaning the :func:`.configure_mappers` function will continue to be
        called when mappers are used, to continue to try to configure all
        available mappers.

        In comparison to the other configure-level events,
        :meth:`.MapperEvents.before_configured`,
        :meth:`.MapperEvents.after_configured`, and
        :meth:`.MapperEvents.mapper_configured`, the
        :meth;`.MapperEvents.before_mapper_configured` event provides for a
        meaningful return value when it is registered with the ``retval=True``
        parameter.

        .. versionadded:: 1.3

        e.g.::

            from sqlalchemy.orm import EXT_SKIP

            Base = declarative_base()

            DontConfigureBase = declarative_base()

            @event.listens_for(
                DontConfigureBase,
                "before_mapper_configured", retval=True, propagate=True)
            def dont_configure(mapper, cls):
                return EXT_SKIP


        .. seealso::

            :meth:`.MapperEvents.before_configured`

            :meth:`.MapperEvents.after_configured`

            :meth:`.MapperEvents.mapper_configured`

        """

    def mapper_configured(self, mapper: Mapper[_O], class_: Type[_O]) -> None:
        r"""Called when a specific mapper has completed its own configuration
        within the scope of the :func:`.configure_mappers` call.

        The :meth:`.MapperEvents.mapper_configured` event is invoked
        for each mapper that is encountered when the
        :func:`_orm.configure_mappers` function proceeds through the current
        list of not-yet-configured mappers.
        :func:`_orm.configure_mappers` is typically invoked
        automatically as mappings are first used, as well as each time
        new mappers have been made available and new mapper use is
        detected.

        When the event is called, the mapper should be in its final
        state, but **not including backrefs** that may be invoked from
        other mappers; they might still be pending within the
        configuration operation.    Bidirectional relationships that
        are instead configured via the
        :paramref:`.orm.relationship.back_populates` argument
        *will* be fully available, since this style of relationship does not
        rely upon other possibly-not-configured mappers to know that they
        exist.

        For an event that is guaranteed to have **all** mappers ready
        to go including backrefs that are defined only on other
        mappings, use the :meth:`.MapperEvents.after_configured`
        event; this event invokes only after all known mappings have been
        fully configured.

        The :meth:`.MapperEvents.mapper_configured` event, unlike
        :meth:`.MapperEvents.before_configured` or
        :meth:`.MapperEvents.after_configured`,
        is called for each mapper/class individually, and the mapper is
        passed to the event itself.  It also is called exactly once for
        a particular mapper.  The event is therefore useful for
        configurational steps that benefit from being invoked just once
        on a specific mapper basis, which don't require that "backref"
        configurations are necessarily ready yet.

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param class\_: the mapped class.

        .. seealso::

            :meth:`.MapperEvents.before_configured`

            :meth:`.MapperEvents.after_configured`

            :meth:`.MapperEvents.before_mapper_configured`

        """
        # TODO: need coverage for this event

    def before_configured(self) -> None:
        """Called before a series of mappers have been configured.

        The :meth:`.MapperEvents.before_configured` event is invoked
        each time the :func:`_orm.configure_mappers` function is
        invoked, before the function has done any of its work.
        :func:`_orm.configure_mappers` is typically invoked
        automatically as mappings are first used, as well as each time
        new mappers have been made available and new mapper use is
        detected.

        This event can **only** be applied to the :class:`_orm.Mapper` class,
        and not to individual mappings or mapped classes. It is only invoked
        for all mappings as a whole::

            from sqlalchemy.orm import Mapper

            @event.listens_for(Mapper, "before_configured")
            def go():
                # ...

        Contrast this event to :meth:`.MapperEvents.after_configured`,
        which is invoked after the series of mappers has been configured,
        as well as :meth:`.MapperEvents.before_mapper_configured`
        and :meth:`.MapperEvents.mapper_configured`, which are both invoked
        on a per-mapper basis.

        Theoretically this event is called once per
        application, but is actually called any time new mappers
        are to be affected by a :func:`_orm.configure_mappers`
        call.   If new mappings are constructed after existing ones have
        already been used, this event will likely be called again.  To ensure
        that a particular event is only called once and no further, the
        ``once=True`` argument (new in 0.9.4) can be applied::

            from sqlalchemy.orm import mapper

            @event.listens_for(mapper, "before_configured", once=True)
            def go():
                # ...


        .. versionadded:: 0.9.3


        .. seealso::

            :meth:`.MapperEvents.before_mapper_configured`

            :meth:`.MapperEvents.mapper_configured`

            :meth:`.MapperEvents.after_configured`

        """

    def after_configured(self) -> None:
        """Called after a series of mappers have been configured.

        The :meth:`.MapperEvents.after_configured` event is invoked
        each time the :func:`_orm.configure_mappers` function is
        invoked, after the function has completed its work.
        :func:`_orm.configure_mappers` is typically invoked
        automatically as mappings are first used, as well as each time
        new mappers have been made available and new mapper use is
        detected.

        Contrast this event to the :meth:`.MapperEvents.mapper_configured`
        event, which is called on a per-mapper basis while the configuration
        operation proceeds; unlike that event, when this event is invoked,
        all cross-configurations (e.g. backrefs) will also have been made
        available for any mappers that were pending.
        Also contrast to :meth:`.MapperEvents.before_configured`,
        which is invoked before the series of mappers has been configured.

        This event can **only** be applied to the :class:`_orm.Mapper` class,
        and not to individual mappings or
        mapped classes.  It is only invoked for all mappings as a whole::

            from sqlalchemy.orm import Mapper

            @event.listens_for(Mapper, "after_configured")
            def go():
                # ...

        Theoretically this event is called once per
        application, but is actually called any time new mappers
        have been affected by a :func:`_orm.configure_mappers`
        call.   If new mappings are constructed after existing ones have
        already been used, this event will likely be called again.  To ensure
        that a particular event is only called once and no further, the
        ``once=True`` argument (new in 0.9.4) can be applied::

            from sqlalchemy.orm import mapper

            @event.listens_for(mapper, "after_configured", once=True)
            def go():
                # ...

        .. seealso::

            :meth:`.MapperEvents.before_mapper_configured`

            :meth:`.MapperEvents.mapper_configured`

            :meth:`.MapperEvents.before_configured`

        """

    def before_insert(
        self, mapper: Mapper[_O], connection: Connection, target: _O
    ) -> None:
        """Receive an object instance before an INSERT statement
        is emitted corresponding to that instance.

        .. note:: this event **only** applies to the
           :ref:`session flush operation <session_flushing>`
           and does **not** apply to the ORM DML operations described at
           :ref:`orm_expression_update_delete`.  To intercept ORM
           DML events, use :meth:`_orm.SessionEvents.do_orm_execute`.

        This event is used to modify local, non-object related
        attributes on the instance before an INSERT occurs, as well
        as to emit additional SQL statements on the given
        connection.

        The event is often called for a batch of objects of the
        same class before their INSERT statements are emitted at
        once in a later step. In the extremely rare case that
        this is not desirable, the :class:`_orm.Mapper` object can be
        configured with ``batch=False``, which will cause
        batches of instances to be broken up into individual
        (and more poorly performing) event->persist->event
        steps.

        .. warning::

            Mapper-level flush events only allow **very limited operations**,
            on attributes local to the row being operated upon only,
            as well as allowing any SQL to be emitted on the given
            :class:`_engine.Connection`.  **Please read fully** the notes
            at :ref:`session_persistence_mapper` for guidelines on using
            these methods; generally, the :meth:`.SessionEvents.before_flush`
            method should be preferred for general on-flush changes.

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param connection: the :class:`_engine.Connection` being used to
         emit INSERT statements for this instance.  This
         provides a handle into the current transaction on the
         target database specific to this instance.
        :param target: the mapped instance being persisted.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :return: No return value is supported by this event.

        .. seealso::

            :ref:`session_persistence_events`

        """

    def after_insert(
        self, mapper: Mapper[_O], connection: Connection, target: _O
    ) -> None:
        """Receive an object instance after an INSERT statement
        is emitted corresponding to that instance.

        .. note:: this event **only** applies to the
           :ref:`session flush operation <session_flushing>`
           and does **not** apply to the ORM DML operations described at
           :ref:`orm_expression_update_delete`.  To intercept ORM
           DML events, use :meth:`_orm.SessionEvents.do_orm_execute`.

        This event is used to modify in-Python-only
        state on the instance after an INSERT occurs, as well
        as to emit additional SQL statements on the given
        connection.

        The event is often called for a batch of objects of the
        same class after their INSERT statements have been
        emitted at once in a previous step. In the extremely
        rare case that this is not desirable, the
        :class:`_orm.Mapper` object can be configured with ``batch=False``,
        which will cause batches of instances to be broken up
        into individual (and more poorly performing)
        event->persist->event steps.

        .. warning::

            Mapper-level flush events only allow **very limited operations**,
            on attributes local to the row being operated upon only,
            as well as allowing any SQL to be emitted on the given
            :class:`_engine.Connection`.  **Please read fully** the notes
            at :ref:`session_persistence_mapper` for guidelines on using
            these methods; generally, the :meth:`.SessionEvents.before_flush`
            method should be preferred for general on-flush changes.

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param connection: the :class:`_engine.Connection` being used to
         emit INSERT statements for this instance.  This
         provides a handle into the current transaction on the
         target database specific to this instance.
        :param target: the mapped instance being persisted.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :return: No return value is supported by this event.

        .. seealso::

            :ref:`session_persistence_events`

        """

    def before_update(
        self, mapper: Mapper[_O], connection: Connection, target: _O
    ) -> None:
        """Receive an object instance before an UPDATE statement
        is emitted corresponding to that instance.

        .. note:: this event **only** applies to the
           :ref:`session flush operation <session_flushing>`
           and does **not** apply to the ORM DML operations described at
           :ref:`orm_expression_update_delete`.  To intercept ORM
           DML events, use :meth:`_orm.SessionEvents.do_orm_execute`.

        This event is used to modify local, non-object related
        attributes on the instance before an UPDATE occurs, as well
        as to emit additional SQL statements on the given
        connection.

        This method is called for all instances that are
        marked as "dirty", *even those which have no net changes
        to their column-based attributes*. An object is marked
        as dirty when any of its column-based attributes have a
        "set attribute" operation called or when any of its
        collections are modified. If, at update time, no
        column-based attributes have any net changes, no UPDATE
        statement will be issued. This means that an instance
        being sent to :meth:`~.MapperEvents.before_update` is
        *not* a guarantee that an UPDATE statement will be
        issued, although you can affect the outcome here by
        modifying attributes so that a net change in value does
        exist.

        To detect if the column-based attributes on the object have net
        changes, and will therefore generate an UPDATE statement, use
        ``object_session(instance).is_modified(instance,
        include_collections=False)``.

        The event is often called for a batch of objects of the
        same class before their UPDATE statements are emitted at
        once in a later step. In the extremely rare case that
        this is not desirable, the :class:`_orm.Mapper` can be
        configured with ``batch=False``, which will cause
        batches of instances to be broken up into individual
        (and more poorly performing) event->persist->event
        steps.

        .. warning::

            Mapper-level flush events only allow **very limited operations**,
            on attributes local to the row being operated upon only,
            as well as allowing any SQL to be emitted on the given
            :class:`_engine.Connection`.  **Please read fully** the notes
            at :ref:`session_persistence_mapper` for guidelines on using
            these methods; generally, the :meth:`.SessionEvents.before_flush`
            method should be preferred for general on-flush changes.

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param connection: the :class:`_engine.Connection` being used to
         emit UPDATE statements for this instance.  This
         provides a handle into the current transaction on the
         target database specific to this instance.
        :param target: the mapped instance being persisted.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :return: No return value is supported by this event.

        .. seealso::

            :ref:`session_persistence_events`

        """

    def after_update(
        self, mapper: Mapper[_O], connection: Connection, target: _O
    ) -> None:
        """Receive an object instance after an UPDATE statement
        is emitted corresponding to that instance.

        .. note:: this event **only** applies to the
           :ref:`session flush operation <session_flushing>`
           and does **not** apply to the ORM DML operations described at
           :ref:`orm_expression_update_delete`.  To intercept ORM
           DML events, use :meth:`_orm.SessionEvents.do_orm_execute`.

        This event is used to modify in-Python-only
        state on the instance after an UPDATE occurs, as well
        as to emit additional SQL statements on the given
        connection.

        This method is called for all instances that are
        marked as "dirty", *even those which have no net changes
        to their column-based attributes*, and for which
        no UPDATE statement has proceeded. An object is marked
        as dirty when any of its column-based attributes have a
        "set attribute" operation called or when any of its
        collections are modified. If, at update time, no
        column-based attributes have any net changes, no UPDATE
        statement will be issued. This means that an instance
        being sent to :meth:`~.MapperEvents.after_update` is
        *not* a guarantee that an UPDATE statement has been
        issued.

        To detect if the column-based attributes on the object have net
        changes, and therefore resulted in an UPDATE statement, use
        ``object_session(instance).is_modified(instance,
        include_collections=False)``.

        The event is often called for a batch of objects of the
        same class after their UPDATE statements have been emitted at
        once in a previous step. In the extremely rare case that
        this is not desirable, the :class:`_orm.Mapper` can be
        configured with ``batch=False``, which will cause
        batches of instances to be broken up into individual
        (and more poorly performing) event->persist->event
        steps.

        .. warning::

            Mapper-level flush events only allow **very limited operations**,
            on attributes local to the row being operated upon only,
            as well as allowing any SQL to be emitted on the given
            :class:`_engine.Connection`.  **Please read fully** the notes
            at :ref:`session_persistence_mapper` for guidelines on using
            these methods; generally, the :meth:`.SessionEvents.before_flush`
            method should be preferred for general on-flush changes.

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param connection: the :class:`_engine.Connection` being used to
         emit UPDATE statements for this instance.  This
         provides a handle into the current transaction on the
         target database specific to this instance.
        :param target: the mapped instance being persisted.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :return: No return value is supported by this event.

        .. seealso::

            :ref:`session_persistence_events`

        """

    def before_delete(
        self, mapper: Mapper[_O], connection: Connection, target: _O
    ) -> None:
        """Receive an object instance before a DELETE statement
        is emitted corresponding to that instance.

        .. note:: this event **only** applies to the
           :ref:`session flush operation <session_flushing>`
           and does **not** apply to the ORM DML operations described at
           :ref:`orm_expression_update_delete`.  To intercept ORM
           DML events, use :meth:`_orm.SessionEvents.do_orm_execute`.

        This event is used to emit additional SQL statements on
        the given connection as well as to perform application
        specific bookkeeping related to a deletion event.

        The event is often called for a batch of objects of the
        same class before their DELETE statements are emitted at
        once in a later step.

        .. warning::

            Mapper-level flush events only allow **very limited operations**,
            on attributes local to the row being operated upon only,
            as well as allowing any SQL to be emitted on the given
            :class:`_engine.Connection`.  **Please read fully** the notes
            at :ref:`session_persistence_mapper` for guidelines on using
            these methods; generally, the :meth:`.SessionEvents.before_flush`
            method should be preferred for general on-flush changes.

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param connection: the :class:`_engine.Connection` being used to
         emit DELETE statements for this instance.  This
         provides a handle into the current transaction on the
         target database specific to this instance.
        :param target: the mapped instance being deleted.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :return: No return value is supported by this event.

        .. seealso::

            :ref:`session_persistence_events`

        """

    def after_delete(
        self, mapper: Mapper[_O], connection: Connection, target: _O
    ) -> None:
        """Receive an object instance after a DELETE statement
        has been emitted corresponding to that instance.

        .. note:: this event **only** applies to the
           :ref:`session flush operation <session_flushing>`
           and does **not** apply to the ORM DML operations described at
           :ref:`orm_expression_update_delete`.  To intercept ORM
           DML events, use :meth:`_orm.SessionEvents.do_orm_execute`.

        This event is used to emit additional SQL statements on
        the given connection as well as to perform application
        specific bookkeeping related to a deletion event.

        The event is often called for a batch of objects of the
        same class after their DELETE statements have been emitted at
        once in a previous step.

        .. warning::

            Mapper-level flush events only allow **very limited operations**,
            on attributes local to the row being operated upon only,
            as well as allowing any SQL to be emitted on the given
            :class:`_engine.Connection`.  **Please read fully** the notes
            at :ref:`session_persistence_mapper` for guidelines on using
            these methods; generally, the :meth:`.SessionEvents.before_flush`
            method should be preferred for general on-flush changes.

        :param mapper: the :class:`_orm.Mapper` which is the target
         of this event.
        :param connection: the :class:`_engine.Connection` being used to
         emit DELETE statements for this instance.  This
         provides a handle into the current transaction on the
         target database specific to this instance.
        :param target: the mapped instance being deleted.  If
         the event is configured with ``raw=True``, this will
         instead be the :class:`.InstanceState` state-management
         object associated with the instance.
        :return: No return value is supported by this event.

        .. seealso::

            :ref:`session_persistence_events`

        """


class _MapperEventsHold(_EventsHold[_ET]):
    all_holds = weakref.WeakKeyDictionary()

    def resolve(
        self, class_: Union[Type[_T], _InternalEntityType[_T]]
    ) -> Optional[Mapper[_T]]:
        return _mapper_or_none(class_)

    class HoldMapperEvents(_EventsHold.HoldEvents[_ET], MapperEvents):  # type: ignore [misc] # noqa: E501
        pass

    dispatch = event.dispatcher(HoldMapperEvents)


_sessionevents_lifecycle_event_names: Set[str] = set()


class SessionEvents(event.Events[Session]):
    """Define events specific to :class:`.Session` lifecycle.

    e.g.::

        from sqlalchemy import event
        from sqlalchemy.orm import sessionmaker

        def my_before_commit(session):
            print("before commit!")

        Session = sessionmaker()

        event.listen(Session, "before_commit", my_before_commit)

    The :func:`~.event.listen` function will accept
    :class:`.Session` objects as well as the return result
    of :class:`~.sessionmaker()` and :class:`~.scoped_session()`.

    Additionally, it accepts the :class:`.Session` class which
    will apply listeners to all :class:`.Session` instances
    globally.

    :param raw=False: When True, the "target" argument passed
       to applicable event listener functions that work on individual
       objects will be the instance's :class:`.InstanceState` management
       object, rather than the mapped instance itself.

       .. versionadded:: 1.3.14

    :param restore_load_context=False: Applies to the
       :meth:`.SessionEvents.loaded_as_persistent` event.  Restores the loader
       context of the object when the event hook is complete, so that ongoing
       eager load operations continue to target the object appropriately.  A
       warning is emitted if the object is moved to a new loader context from
       within this event if this flag is not set.

       .. versionadded:: 1.3.14

    """

    _target_class_doc = "SomeSessionClassOrObject"

    _dispatch_target = Session

    def _lifecycle_event(  # type: ignore [misc]
        fn: Callable[[SessionEvents, Session, Any], None]
    ) -> Callable[[SessionEvents, Session, Any], None]:
        _sessionevents_lifecycle_event_names.add(fn.__name__)
        return fn

    @classmethod
    def _accept_with(  # type: ignore [return]
        cls, target: Any, identifier: str
    ) -> Union[Session, type]:
        if isinstance(target, scoped_session):

            target = target.session_factory
            if not isinstance(target, sessionmaker) and (
                not isinstance(target, type) or not issubclass(target, Session)
            ):
                raise exc.ArgumentError(
                    "Session event listen on a scoped_session "
                    "requires that its creation callable "
                    "is associated with the Session class."
                )

        if isinstance(target, sessionmaker):
            return target.class_
        elif isinstance(target, type):
            if issubclass(target, scoped_session):
                return Session
            elif issubclass(target, Session):
                return target
        elif isinstance(target, Session):
            return target
        elif hasattr(target, "_no_async_engine_events"):
            target._no_async_engine_events()
        else:
            # allows alternate SessionEvents-like-classes to be consulted
            return event.Events._accept_with(target, identifier)  # type: ignore [return-value] # noqa: E501

    @classmethod
    def _listen(
        cls,
        event_key: Any,
        *,
        raw: bool = False,
        restore_load_context: bool = False,
        **kw: Any,
    ) -> None:
        is_instance_event = (
            event_key.identifier in _sessionevents_lifecycle_event_names
        )

        if is_instance_event:
            if not raw or restore_load_context:

                fn = event_key._listen_fn

                def wrap(
                    session: Session,
                    state: InstanceState[_O],
                    *arg: Any,
                    **kw: Any,
                ) -> Optional[Any]:
                    if not raw:
                        target = state.obj()
                        if target is None:
                            # existing behavior is that if the object is
                            # garbage collected, no event is emitted
                            return None
                    else:
                        target = state  # type: ignore [assignment]
                    if restore_load_context:
                        runid = state.runid
                    try:
                        return fn(session, target, *arg, **kw)
                    finally:
                        if restore_load_context:
                            state.runid = runid

                event_key = event_key.with_wrapper(wrap)

        event_key.base_listen(**kw)

    def do_orm_execute(self, orm_execute_state: ORMExecuteState) -> None:
        """Intercept statement executions that occur on behalf of an
        ORM :class:`.Session` object.

        This event is invoked for all top-level SQL statements invoked from the
        :meth:`_orm.Session.execute` method, as well as related methods such as
        :meth:`_orm.Session.scalars` and :meth:`_orm.Session.scalar`. As of
        SQLAlchemy 1.4, all ORM queries that run through the
        :meth:`_orm.Session.execute` method as well as related methods
        :meth:`_orm.Session.scalars`, :meth:`_orm.Session.scalar` etc.
        will participate in this event.
        This event hook does **not** apply to the queries that are
        emitted internally within the ORM flush process, i.e. the
        process described at :ref:`session_flushing`.

        .. note::  The :meth:`_orm.SessionEvents.do_orm_execute` event hook
           is triggered **for ORM statement executions only**, meaning those
           invoked via the :meth:`_orm.Session.execute` and similar methods on
           the :class:`_orm.Session` object. It does **not** trigger for
           statements that are invoked by SQLAlchemy Core only, i.e. statements
           invoked directly using :meth:`_engine.Connection.execute` or
           otherwise originating from an :class:`_engine.Engine` object without
           any :class:`_orm.Session` involved. To intercept **all** SQL
           executions regardless of whether the Core or ORM APIs are in use,
           see the event hooks at :class:`.ConnectionEvents`, such as
           :meth:`.ConnectionEvents.before_execute` and
           :meth:`.ConnectionEvents.before_cursor_execute`.

           Also, this event hook does **not** apply to queries that are
           emitted internally within the ORM flush process,
           i.e. the process described at :ref:`session_flushing`; to
           intercept steps within the flush process, see the event
           hooks described at :ref:`session_persistence_events` as
           well as :ref:`session_persistence_mapper`.

        This event is a ``do_`` event, meaning it has the capability to replace
        the operation that the :meth:`_orm.Session.execute` method normally
        performs.  The intended use for this includes sharding and
        result-caching schemes which may seek to invoke the same statement
        across  multiple database connections, returning a result that is
        merged from each of them, or which don't invoke the statement at all,
        instead returning data from a cache.

        The hook intends to replace the use of the
        ``Query._execute_and_instances`` method that could be subclassed prior
        to SQLAlchemy 1.4.

        :param orm_execute_state: an instance of :class:`.ORMExecuteState`
         which contains all information about the current execution, as well
         as helper functions used to derive other commonly required
         information.   See that object for details.

        .. seealso::

            :ref:`session_execute_events` - top level documentation on how
            to use :meth:`_orm.SessionEvents.do_orm_execute`

            :class:`.ORMExecuteState` - the object passed to the
            :meth:`_orm.SessionEvents.do_orm_execute` event which contains
            all information about the statement to be invoked.  It also
            provides an interface to extend the current statement, options,
            and parameters as well as an option that allows programmatic
            invocation of the statement at any point.

            :ref:`examples_session_orm_events` - includes examples of using
            :meth:`_orm.SessionEvents.do_orm_execute`

            :ref:`examples_caching` - an example of how to integrate
            Dogpile caching with the ORM :class:`_orm.Session` making use
            of the :meth:`_orm.SessionEvents.do_orm_execute` event hook.

            :ref:`examples_sharding` - the Horizontal Sharding example /
            extension relies upon the
            :meth:`_orm.SessionEvents.do_orm_execute` event hook to invoke a
            SQL statement on multiple backends and return a merged result.


        .. versionadded:: 1.4

        """

    def after_transaction_create(
        self, session: Session, transaction: SessionTransaction
    ) -> None:
        """Execute when a new :class:`.SessionTransaction` is created.

        This event differs from :meth:`~.SessionEvents.after_begin`
        in that it occurs for each :class:`.SessionTransaction`
        overall, as opposed to when transactions are begun
        on individual database connections.  It is also invoked
        for nested transactions and subtransactions, and is always
        matched by a corresponding
        :meth:`~.SessionEvents.after_transaction_end` event
        (assuming normal operation of the :class:`.Session`).

        :param session: the target :class:`.Session`.
        :param transaction: the target :class:`.SessionTransaction`.

         To detect if this is the outermost
         :class:`.SessionTransaction`, as opposed to a "subtransaction" or a
         SAVEPOINT, test that the :attr:`.SessionTransaction.parent` attribute
         is ``None``::

                @event.listens_for(session, "after_transaction_create")
                def after_transaction_create(session, transaction):
                    if transaction.parent is None:
                        # work with top-level transaction

         To detect if the :class:`.SessionTransaction` is a SAVEPOINT, use the
         :attr:`.SessionTransaction.nested` attribute::

                @event.listens_for(session, "after_transaction_create")
                def after_transaction_create(session, transaction):
                    if transaction.nested:
                        # work with SAVEPOINT transaction


        .. seealso::

            :class:`.SessionTransaction`

            :meth:`~.SessionEvents.after_transaction_end`

        """

    def after_transaction_end(
        self, session: Session, transaction: SessionTransaction
    ) -> None:
        """Execute when the span of a :class:`.SessionTransaction` ends.

        This event differs from :meth:`~.SessionEvents.after_commit`
        in that it corresponds to all :class:`.SessionTransaction`
        objects in use, including those for nested transactions
        and subtransactions, and is always matched by a corresponding
        :meth:`~.SessionEvents.after_transaction_create` event.

        :param session: the target :class:`.Session`.
        :param transaction: the target :class:`.SessionTransaction`.

         To detect if this is the outermost
         :class:`.SessionTransaction`, as opposed to a "subtransaction" or a
         SAVEPOINT, test that the :attr:`.SessionTransaction.parent` attribute
         is ``None``::

                @event.listens_for(session, "after_transaction_create")
                def after_transaction_end(session, transaction):
                    if transaction.parent is None:
                        # work with top-level transaction

         To detect if the :class:`.SessionTransaction` is a SAVEPOINT, use the
         :attr:`.SessionTransaction.nested` attribute::

                @event.listens_for(session, "after_transaction_create")
                def after_transaction_end(session, transaction):
                    if transaction.nested:
                        # work with SAVEPOINT transaction


        .. seealso::

            :class:`.SessionTransaction`

            :meth:`~.SessionEvents.after_transaction_create`

        """

    def before_commit(self, session: Session) -> None:
        """Execute before commit is called.

        .. note::

            The :meth:`~.SessionEvents.before_commit` hook is *not* per-flush,
            that is, the :class:`.Session` can emit SQL to the database
            many times within the scope of a transaction.
            For interception of these events, use the
            :meth:`~.SessionEvents.before_flush`,
            :meth:`~.SessionEvents.after_flush`, or
            :meth:`~.SessionEvents.after_flush_postexec`
            events.

        :param session: The target :class:`.Session`.

        .. seealso::

            :meth:`~.SessionEvents.after_commit`

            :meth:`~.SessionEvents.after_begin`

            :meth:`~.SessionEvents.after_transaction_create`

            :meth:`~.SessionEvents.after_transaction_end`

        """

    def after_commit(self, session: Session) -> None:
        """Execute after a commit has occurred.

        .. note::

            The :meth:`~.SessionEvents.after_commit` hook is *not* per-flush,
            that is, the :class:`.Session` can emit SQL to the database
            many times within the scope of a transaction.
            For interception of these events, use the
            :meth:`~.SessionEvents.before_flush`,
            :meth:`~.SessionEvents.after_flush`, or
            :meth:`~.SessionEvents.after_flush_postexec`
            events.

        .. note::

            The :class:`.Session` is not in an active transaction
            when the :meth:`~.SessionEvents.after_commit` event is invoked,
            and therefore can not emit SQL.  To emit SQL corresponding to
            every transaction, use the :meth:`~.SessionEvents.before_commit`
            event.

        :param session: The target :class:`.Session`.

        .. seealso::

            :meth:`~.SessionEvents.before_commit`

            :meth:`~.SessionEvents.after_begin`

            :meth:`~.SessionEvents.after_transaction_create`

            :meth:`~.SessionEvents.after_transaction_end`

        """

    def after_rollback(self, session: Session) -> None:
        """Execute after a real DBAPI rollback has occurred.

        Note that this event only fires when the *actual* rollback against
        the database occurs - it does *not* fire each time the
        :meth:`.Session.rollback` method is called, if the underlying
        DBAPI transaction has already been rolled back.  In many
        cases, the :class:`.Session` will not be in
        an "active" state during this event, as the current
        transaction is not valid.   To acquire a :class:`.Session`
        which is active after the outermost rollback has proceeded,
        use the :meth:`.SessionEvents.after_soft_rollback` event, checking the
        :attr:`.Session.is_active` flag.

        :param session: The target :class:`.Session`.

        """

    def after_soft_rollback(
        self, session: Session, previous_transaction: SessionTransaction
    ) -> None:
        """Execute after any rollback has occurred, including "soft"
        rollbacks that don't actually emit at the DBAPI level.

        This corresponds to both nested and outer rollbacks, i.e.
        the innermost rollback that calls the DBAPI's
        rollback() method, as well as the enclosing rollback
        calls that only pop themselves from the transaction stack.

        The given :class:`.Session` can be used to invoke SQL and
        :meth:`.Session.query` operations after an outermost rollback
        by first checking the :attr:`.Session.is_active` flag::

            @event.listens_for(Session, "after_soft_rollback")
            def do_something(session, previous_transaction):
                if session.is_active:
                    session.execute("select * from some_table")

        :param session: The target :class:`.Session`.
        :param previous_transaction: The :class:`.SessionTransaction`
         transactional marker object which was just closed.   The current
         :class:`.SessionTransaction` for the given :class:`.Session` is
         available via the :attr:`.Session.transaction` attribute.

        """

    def before_flush(
        self,
        session: Session,
        flush_context: UOWTransaction,
        instances: Optional[Sequence[_O]],
    ) -> None:
        """Execute before flush process has started.

        :param session: The target :class:`.Session`.
        :param flush_context: Internal :class:`.UOWTransaction` object
         which handles the details of the flush.
        :param instances: Usually ``None``, this is the collection of
         objects which can be passed to the :meth:`.Session.flush` method
         (note this usage is deprecated).

        .. seealso::

            :meth:`~.SessionEvents.after_flush`

            :meth:`~.SessionEvents.after_flush_postexec`

            :ref:`session_persistence_events`

        """

    def after_flush(
        self, session: Session, flush_context: UOWTransaction
    ) -> None:
        """Execute after flush has completed, but before commit has been
        called.

        Note that the session's state is still in pre-flush, i.e. 'new',
        'dirty', and 'deleted' lists still show pre-flush state as well
        as the history settings on instance attributes.

        .. warning:: This event runs after the :class:`.Session` has emitted
           SQL to modify the database, but **before** it has altered its
           internal state to reflect those changes, including that newly
           inserted objects are placed into the identity map.  ORM operations
           emitted within this event such as loads of related items
           may produce new identity map entries that will immediately
           be replaced, sometimes causing confusing results.  SQLAlchemy will
           emit a warning for this condition as of version 1.3.9.

        :param session: The target :class:`.Session`.
        :param flush_context: Internal :class:`.UOWTransaction` object
         which handles the details of the flush.

        .. seealso::

            :meth:`~.SessionEvents.before_flush`

            :meth:`~.SessionEvents.after_flush_postexec`

            :ref:`session_persistence_events`

        """

    def after_flush_postexec(
        self, session: Session, flush_context: UOWTransaction
    ) -> None:
        """Execute after flush has completed, and after the post-exec
        state occurs.

        This will be when the 'new', 'dirty', and 'deleted' lists are in
        their final state.  An actual commit() may or may not have
        occurred, depending on whether or not the flush started its own
        transaction or participated in a larger transaction.

        :param session: The target :class:`.Session`.
        :param flush_context: Internal :class:`.UOWTransaction` object
         which handles the details of the flush.


        .. seealso::

            :meth:`~.SessionEvents.before_flush`

            :meth:`~.SessionEvents.after_flush`

            :ref:`session_persistence_events`

        """

    def after_begin(
        self,
        session: Session,
        transaction: SessionTransaction,
        connection: Connection,
    ) -> None:
        """Execute after a transaction is begun on a connection

        :param session: The target :class:`.Session`.
        :param transaction: The :class:`.SessionTransaction`.
        :param connection: The :class:`_engine.Connection` object
         which will be used for SQL statements.

        .. seealso::

            :meth:`~.SessionEvents.before_commit`

            :meth:`~.SessionEvents.after_commit`

            :meth:`~.SessionEvents.after_transaction_create`

            :meth:`~.SessionEvents.after_transaction_end`

        """

    @_lifecycle_event
    def before_attach(self, session: Session, instance: _O) -> None:
        """Execute before an instance is attached to a session.

        This is called before an add, delete or merge causes
        the object to be part of the session.

        .. seealso::

            :meth:`~.SessionEvents.after_attach`

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def after_attach(self, session: Session, instance: _O) -> None:
        """Execute after an instance is attached to a session.

        This is called after an add, delete or merge.

        .. note::

           As of 0.8, this event fires off *after* the item
           has been fully associated with the session, which is
           different than previous releases.  For event
           handlers that require the object not yet
           be part of session state (such as handlers which
           may autoflush while the target object is not
           yet complete) consider the
           new :meth:`.before_attach` event.

        .. seealso::

            :meth:`~.SessionEvents.before_attach`

            :ref:`session_lifecycle_events`

        """

    @event._legacy_signature(
        "0.9",
        ["session", "query", "query_context", "result"],
        lambda update_context: (
            update_context.session,
            update_context.query,
            None,
            update_context.result,
        ),
    )
    def after_bulk_update(self, update_context: _O) -> None:
        """Event for after the legacy :meth:`_orm.Query.update` method
        has been called.

        .. legacy:: The :meth:`_orm.SessionEvents.after_bulk_update` method
           is a legacy event hook as of SQLAlchemy 2.0.   The event
           **does not participate** in :term:`2.0 style` invocations
           using :func:`_dml.update` documented at
           :ref:`orm_queryguide_update_delete_where`.  For 2.0 style use,
           the :meth:`_orm.SessionEvents.do_orm_execute` hook will intercept
           these calls.

        :param update_context: an "update context" object which contains
         details about the update, including these attributes:

            * ``session`` - the :class:`.Session` involved
            * ``query`` -the :class:`_query.Query`
              object that this update operation
              was called upon.
            * ``values`` The "values" dictionary that was passed to
              :meth:`_query.Query.update`.
            * ``result`` the :class:`_engine.CursorResult`
              returned as a result of the
              bulk UPDATE operation.

        .. versionchanged:: 1.4 the update_context no longer has a
           ``QueryContext`` object associated with it.

        .. seealso::

            :meth:`.QueryEvents.before_compile_update`

            :meth:`.SessionEvents.after_bulk_delete`

        """

    @event._legacy_signature(
        "0.9",
        ["session", "query", "query_context", "result"],
        lambda delete_context: (
            delete_context.session,
            delete_context.query,
            None,
            delete_context.result,
        ),
    )
    def after_bulk_delete(self, delete_context: _O) -> None:
        """Event for after the legacy :meth:`_orm.Query.delete` method
        has been called.

        .. legacy:: The :meth:`_orm.SessionEvents.after_bulk_delete` method
           is a legacy event hook as of SQLAlchemy 2.0.   The event
           **does not participate** in :term:`2.0 style` invocations
           using :func:`_dml.delete` documented at
           :ref:`orm_queryguide_update_delete_where`.  For 2.0 style use,
           the :meth:`_orm.SessionEvents.do_orm_execute` hook will intercept
           these calls.

        :param delete_context: a "delete context" object which contains
         details about the update, including these attributes:

            * ``session`` - the :class:`.Session` involved
            * ``query`` -the :class:`_query.Query`
              object that this update operation
              was called upon.
            * ``result`` the :class:`_engine.CursorResult`
              returned as a result of the
              bulk DELETE operation.

        .. versionchanged:: 1.4 the update_context no longer has a
           ``QueryContext`` object associated with it.

        .. seealso::

            :meth:`.QueryEvents.before_compile_delete`

            :meth:`.SessionEvents.after_bulk_update`

        """

    @_lifecycle_event
    def transient_to_pending(self, session: Session, instance: _O) -> None:
        """Intercept the "transient to pending" transition for a specific
        object.

        This event is a specialization of the
        :meth:`.SessionEvents.after_attach` event which is only invoked
        for this specific transition.  It is invoked typically during the
        :meth:`.Session.add` call.

        :param session: target :class:`.Session`

        :param instance: the ORM-mapped instance being operated upon.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def pending_to_transient(self, session: Session, instance: _O) -> None:
        """Intercept the "pending to transient" transition for a specific
        object.

        This less common transition occurs when an pending object that has
        not been flushed is evicted from the session; this can occur
        when the :meth:`.Session.rollback` method rolls back the transaction,
        or when the :meth:`.Session.expunge` method is used.

        :param session: target :class:`.Session`

        :param instance: the ORM-mapped instance being operated upon.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def persistent_to_transient(self, session: Session, instance: _O) -> None:
        """Intercept the "persistent to transient" transition for a specific
        object.

        This less common transition occurs when an pending object that has
        has been flushed is evicted from the session; this can occur
        when the :meth:`.Session.rollback` method rolls back the transaction.

        :param session: target :class:`.Session`

        :param instance: the ORM-mapped instance being operated upon.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def pending_to_persistent(self, session: Session, instance: _O) -> None:
        """Intercept the "pending to persistent"" transition for a specific
        object.

        This event is invoked within the flush process, and is
        similar to scanning the :attr:`.Session.new` collection within
        the :meth:`.SessionEvents.after_flush` event.  However, in this
        case the object has already been moved to the persistent state
        when the event is called.

        :param session: target :class:`.Session`

        :param instance: the ORM-mapped instance being operated upon.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def detached_to_persistent(self, session: Session, instance: _O) -> None:
        """Intercept the "detached to persistent" transition for a specific
        object.

        This event is a specialization of the
        :meth:`.SessionEvents.after_attach` event which is only invoked
        for this specific transition.  It is invoked typically during the
        :meth:`.Session.add` call, as well as during the
        :meth:`.Session.delete` call if the object was not previously
        associated with the
        :class:`.Session` (note that an object marked as "deleted" remains
        in the "persistent" state until the flush proceeds).

        .. note::

            If the object becomes persistent as part of a call to
            :meth:`.Session.delete`, the object is **not** yet marked as
            deleted when this event is called.  To detect deleted objects,
            check the ``deleted`` flag sent to the
            :meth:`.SessionEvents.persistent_to_detached` to event after the
            flush proceeds, or check the :attr:`.Session.deleted` collection
            within the :meth:`.SessionEvents.before_flush` event if deleted
            objects need to be intercepted before the flush.

        :param session: target :class:`.Session`

        :param instance: the ORM-mapped instance being operated upon.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def loaded_as_persistent(self, session: Session, instance: _O) -> None:
        """Intercept the "loaded as persistent" transition for a specific
        object.

        This event is invoked within the ORM loading process, and is invoked
        very similarly to the :meth:`.InstanceEvents.load` event.  However,
        the event here is linkable to a :class:`.Session` class or instance,
        rather than to a mapper or class hierarchy, and integrates
        with the other session lifecycle events smoothly.  The object
        is guaranteed to be present in the session's identity map when
        this event is called.

        .. note:: This event is invoked within the loader process before
           eager loaders may have been completed, and the object's state may
           not be complete.  Additionally, invoking row-level refresh
           operations on the object will place the object into a new loader
           context, interfering with the existing load context.   See the note
           on :meth:`.InstanceEvents.load` for background on making use of the
           :paramref:`.SessionEvents.restore_load_context` parameter, which
           works in the same manner as that of
           :paramref:`.InstanceEvents.restore_load_context`, in  order to
           resolve this scenario.

        :param session: target :class:`.Session`

        :param instance: the ORM-mapped instance being operated upon.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def persistent_to_deleted(self, session: Session, instance: _O) -> None:
        """Intercept the "persistent to deleted" transition for a specific
        object.

        This event is invoked when a persistent object's identity
        is deleted from the database within a flush, however the object
        still remains associated with the :class:`.Session` until the
        transaction completes.

        If the transaction is rolled back, the object moves again
        to the persistent state, and the
        :meth:`.SessionEvents.deleted_to_persistent` event is called.
        If the transaction is committed, the object becomes detached,
        which will emit the :meth:`.SessionEvents.deleted_to_detached`
        event.

        Note that while the :meth:`.Session.delete` method is the primary
        public interface to mark an object as deleted, many objects
        get deleted due to cascade rules, which are not always determined
        until flush time.  Therefore, there's no way to catch
        every object that will be deleted until the flush has proceeded.
        the :meth:`.SessionEvents.persistent_to_deleted` event is therefore
        invoked at the end of a flush.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def deleted_to_persistent(self, session: Session, instance: _O) -> None:
        """Intercept the "deleted to persistent" transition for a specific
        object.

        This transition occurs only when an object that's been deleted
        successfully in a flush is restored due to a call to
        :meth:`.Session.rollback`.   The event is not called under
        any other circumstances.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def deleted_to_detached(self, session: Session, instance: _O) -> None:
        """Intercept the "deleted to detached" transition for a specific
        object.

        This event is invoked when a deleted object is evicted
        from the session.   The typical case when this occurs is when
        the transaction for a :class:`.Session` in which the object
        was deleted is committed; the object moves from the deleted
        state to the detached state.

        It is also invoked for objects that were deleted in a flush
        when the :meth:`.Session.expunge_all` or :meth:`.Session.close`
        events are called, as well as if the object is individually
        expunged from its deleted state via :meth:`.Session.expunge`.

        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """

    @_lifecycle_event
    def persistent_to_detached(self, session: Session, instance: _O) -> None:
        """Intercept the "persistent to detached" transition for a specific
        object.

        This event is invoked when a persistent object is evicted
        from the session.  There are many conditions that cause this
        to happen, including:

        * using a method such as :meth:`.Session.expunge`
          or :meth:`.Session.close`

        * Calling the :meth:`.Session.rollback` method, when the object
          was part of an INSERT statement for that session's transaction


        :param session: target :class:`.Session`

        :param instance: the ORM-mapped instance being operated upon.

        :param deleted: boolean.  If True, indicates this object moved
         to the detached state because it was marked as deleted and flushed.


        .. versionadded:: 1.1

        .. seealso::

            :ref:`session_lifecycle_events`

        """


class AttributeEvents(event.Events[QueryableAttribute[Any]]):
    r"""Define events for object attributes.

    These are typically defined on the class-bound descriptor for the
    target class.

    For example, to register a listener that will receive the
    :meth:`_orm.AttributeEvents.append` event::

        from sqlalchemy import event

        @event.listens_for(MyClass.collection, 'append', propagate=True)
        def my_append_listener(target, value, initiator):
            print("received append event for target: %s" % target)


    Listeners have the option to return a possibly modified version of the
    value, when the :paramref:`.AttributeEvents.retval` flag is passed to
    :func:`.event.listen` or :func:`.event.listens_for`, such as below,
    illustrated using the :meth:`_orm.AttributeEvents.set` event::

        def validate_phone(target, value, oldvalue, initiator):
            "Strip non-numeric characters from a phone number"

            return re.sub(r'\D', '', value)

        # setup listener on UserContact.phone attribute, instructing
        # it to use the return value
        listen(UserContact.phone, 'set', validate_phone, retval=True)

    A validation function like the above can also raise an exception
    such as :exc:`ValueError` to halt the operation.

    The :paramref:`.AttributeEvents.propagate` flag is also important when
    applying listeners to mapped classes that also have mapped subclasses,
    as when using mapper inheritance patterns::


        @event.listens_for(MySuperClass.attr, 'set', propagate=True)
        def receive_set(target, value, initiator):
            print("value set: %s" % target)

    The full list of modifiers available to the :func:`.event.listen`
    and :func:`.event.listens_for` functions are below.

    :param active_history=False: When True, indicates that the
      "set" event would like to receive the "old" value being
      replaced unconditionally, even if this requires firing off
      database loads. Note that ``active_history`` can also be
      set directly via :func:`.column_property` and
      :func:`_orm.relationship`.

    :param propagate=False: When True, the listener function will
      be established not just for the class attribute given, but
      for attributes of the same name on all current subclasses
      of that class, as well as all future subclasses of that
      class, using an additional listener that listens for
      instrumentation events.
    :param raw=False: When True, the "target" argument to the
      event will be the :class:`.InstanceState` management
      object, rather than the mapped instance itself.
    :param retval=False: when True, the user-defined event
      listening must return the "value" argument from the
      function.  This gives the listening function the opportunity
      to change the value that is ultimately used for a "set"
      or "append" event.

    """

    _target_class_doc = "SomeClass.some_attribute"
    _dispatch_target = QueryableAttribute

    @staticmethod
    def _set_dispatch(
        cls: Type[_HasEventsDispatch[Any]], dispatch_cls: Type[_Dispatch[Any]]
    ) -> _Dispatch[Any]:
        dispatch = event.Events._set_dispatch(cls, dispatch_cls)
        dispatch_cls._active_history = False
        return dispatch

    @classmethod
    def _accept_with(
        cls,
        target: Union[QueryableAttribute[Any], Type[QueryableAttribute[Any]]],
        identifier: str,
    ) -> Union[QueryableAttribute[Any], Type[QueryableAttribute[Any]]]:
        # TODO: coverage
        if isinstance(target, interfaces.MapperProperty):
            return getattr(target.parent.class_, target.key)
        else:
            return target

    @classmethod
    def _listen(  # type: ignore [override]
        cls,
        event_key: _EventKey[QueryableAttribute[Any]],
        active_history: bool = False,
        raw: bool = False,
        retval: bool = False,
        propagate: bool = False,
        include_key: bool = False,
    ) -> None:

        target, fn = event_key.dispatch_target, event_key._listen_fn

        if active_history:
            target.dispatch._active_history = True

        if not raw or not retval or not include_key:

            def wrap(target: InstanceState[_O], *arg: Any, **kw: Any) -> Any:
                if not raw:
                    target = target.obj()  # type: ignore [assignment]
                if not retval:
                    if arg:
                        value = arg[0]
                    else:
                        value = None
                    if include_key:
                        fn(target, *arg, **kw)
                    else:
                        fn(target, *arg)
                    return value
                else:
                    if include_key:
                        return fn(target, *arg, **kw)
                    else:
                        return fn(target, *arg)

            event_key = event_key.with_wrapper(wrap)

        event_key.base_listen(propagate=propagate)

        if propagate:
            manager = instrumentation.manager_of_class(target.class_)

            for mgr in manager.subclass_managers(True):  # type: ignore [no-untyped-call] # noqa: E501
                event_key.with_dispatch_target(mgr[target.key]).base_listen(
                    propagate=True
                )
                if active_history:
                    mgr[target.key].dispatch._active_history = True

    def append(
        self,
        target: _O,
        value: _T,
        initiator: Event,
        *,
        key: EventConstants = NO_KEY,
    ) -> Optional[_T]:
        """Receive a collection append event.

        The append event is invoked for each element as it is appended
        to the collection.  This occurs for single-item appends as well
        as for a "bulk replace" operation.

        :param target: the object instance receiving the event.
          If the listener is registered with ``raw=True``, this will
          be the :class:`.InstanceState` object.
        :param value: the value being appended.  If this listener
          is registered with ``retval=True``, the listener
          function must return this value, or a new value which
          replaces it.
        :param initiator: An instance of :class:`.attributes.Event`
          representing the initiation of the event.  May be modified
          from its original value by backref handlers in order to control
          chained event propagation, as well as be inspected for information
          about the source of the event.
        :param key: When the event is established using the
         :paramref:`.AttributeEvents.include_key` parameter set to
         True, this will be the key used in the operation, such as
         ``collection[some_key_or_index] = value``.
         The parameter is not passed
         to the event at all if the the
         :paramref:`.AttributeEvents.include_key`
         was not used to set up the event; this is to allow backwards
         compatibility with existing event handlers that don't include the
         ``key`` parameter.

         .. versionadded:: 2.0

        :return: if the event was registered with ``retval=True``,
         the given value, or a new effective value, should be returned.

        .. seealso::

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.

            :meth:`.AttributeEvents.bulk_replace`

        """

    def append_wo_mutation(
        self,
        target: _O,
        value: _T,
        initiator: Event,
        *,
        key: EventConstants = NO_KEY,
    ) -> None:
        """Receive a collection append event where the collection was not
        actually mutated.

        This event differs from :meth:`_orm.AttributeEvents.append` in that
        it is fired off for de-duplicating collections such as sets and
        dictionaries, when the object already exists in the target collection.
        The event does not have a return value and the identity of the
        given object cannot be changed.

        The event is used for cascading objects into a :class:`_orm.Session`
        when the collection has already been mutated via a backref event.

        :param target: the object instance receiving the event.
          If the listener is registered with ``raw=True``, this will
          be the :class:`.InstanceState` object.
        :param value: the value that would be appended if the object did not
          already exist in the collection.
        :param initiator: An instance of :class:`.attributes.Event`
          representing the initiation of the event.  May be modified
          from its original value by backref handlers in order to control
          chained event propagation, as well as be inspected for information
          about the source of the event.
        :param key: When the event is established using the
         :paramref:`.AttributeEvents.include_key` parameter set to
         True, this will be the key used in the operation, such as
         ``collection[some_key_or_index] = value``.
         The parameter is not passed
         to the event at all if the the
         :paramref:`.AttributeEvents.include_key`
         was not used to set up the event; this is to allow backwards
         compatibility with existing event handlers that don't include the
         ``key`` parameter.

         .. versionadded:: 2.0

        :return: No return value is defined for this event.

        .. versionadded:: 1.4.15

        """

    def bulk_replace(
        self,
        target: _O,
        values: Iterable[_T],
        initiator: Event,
        *,
        keys: Optional[Iterable[EventConstants]] = None,
    ) -> None:
        """Receive a collection 'bulk replace' event.

        This event is invoked for a sequence of values as they are incoming
        to a bulk collection set operation, which can be
        modified in place before the values are treated as ORM objects.
        This is an "early hook" that runs before the bulk replace routine
        attempts to reconcile which objects are already present in the
        collection and which are being removed by the net replace operation.

        It is typical that this method be combined with use of the
        :meth:`.AttributeEvents.append` event.    When using both of these
        events, note that a bulk replace operation will invoke
        the :meth:`.AttributeEvents.append` event for all new items,
        even after :meth:`.AttributeEvents.bulk_replace` has been invoked
        for the collection as a whole.  In order to determine if an
        :meth:`.AttributeEvents.append` event is part of a bulk replace,
        use the symbol :attr:`~.attributes.OP_BULK_REPLACE` to test the
        incoming initiator::

            from sqlalchemy.orm.attributes import OP_BULK_REPLACE

            @event.listens_for(SomeObject.collection, "bulk_replace")
            def process_collection(target, values, initiator):
                values[:] = [_make_value(value) for value in values]

            @event.listens_for(SomeObject.collection, "append", retval=True)
            def process_collection(target, value, initiator):
                # make sure bulk_replace didn't already do it
                if initiator is None or initiator.op is not OP_BULK_REPLACE:
                    return _make_value(value)
                else:
                    return value

        .. versionadded:: 1.2

        :param target: the object instance receiving the event.
          If the listener is registered with ``raw=True``, this will
          be the :class:`.InstanceState` object.
        :param value: a sequence (e.g. a list) of the values being set.  The
          handler can modify this list in place.
        :param initiator: An instance of :class:`.attributes.Event`
          representing the initiation of the event.
        :param keys: When the event is established using the
         :paramref:`.AttributeEvents.include_key` parameter set to
         True, this will be the sequence of keys used in the operation,
         typically only for a dictionary update.  The parameter is not passed
         to the event at all if the the
         :paramref:`.AttributeEvents.include_key`
         was not used to set up the event; this is to allow backwards
         compatibility with existing event handlers that don't include the
         ``key`` parameter.

         .. versionadded:: 2.0

        .. seealso::

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.


        """

    def remove(
        self,
        target: _O,
        value: _T,
        initiator: Event,
        *,
        key: EventConstants = NO_KEY,
    ) -> None:
        """Receive a collection remove event.

        :param target: the object instance receiving the event.
          If the listener is registered with ``raw=True``, this will
          be the :class:`.InstanceState` object.
        :param value: the value being removed.
        :param initiator: An instance of :class:`.attributes.Event`
          representing the initiation of the event.  May be modified
          from its original value by backref handlers in order to control
          chained event propagation.

          .. versionchanged:: 0.9.0 the ``initiator`` argument is now
             passed as a :class:`.attributes.Event` object, and may be
             modified by backref handlers within a chain of backref-linked
             events.
        :param key: When the event is established using the
         :paramref:`.AttributeEvents.include_key` parameter set to
         True, this will be the key used in the operation, such as
         ``del collection[some_key_or_index]``.  The parameter is not passed
         to the event at all if the the
         :paramref:`.AttributeEvents.include_key`
         was not used to set up the event; this is to allow backwards
         compatibility with existing event handlers that don't include the
         ``key`` parameter.

         .. versionadded:: 2.0

        :return: No return value is defined for this event.


        .. seealso::

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.

        """

    def set(
        self, target: _O, value: _T, oldvalue: _T, initiator: Event
    ) -> None:
        """Receive a scalar set event.

        :param target: the object instance receiving the event.
          If the listener is registered with ``raw=True``, this will
          be the :class:`.InstanceState` object.
        :param value: the value being set.  If this listener
          is registered with ``retval=True``, the listener
          function must return this value, or a new value which
          replaces it.
        :param oldvalue: the previous value being replaced.  This
          may also be the symbol ``NEVER_SET`` or ``NO_VALUE``.
          If the listener is registered with ``active_history=True``,
          the previous value of the attribute will be loaded from
          the database if the existing value is currently unloaded
          or expired.
        :param initiator: An instance of :class:`.attributes.Event`
          representing the initiation of the event.  May be modified
          from its original value by backref handlers in order to control
          chained event propagation.

          .. versionchanged:: 0.9.0 the ``initiator`` argument is now
             passed as a :class:`.attributes.Event` object, and may be
             modified by backref handlers within a chain of backref-linked
             events.

        :return: if the event was registered with ``retval=True``,
         the given value, or a new effective value, should be returned.

        .. seealso::

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.

        """

    def init_scalar(
        self, target: _O, value: _T, dict_: Dict[Any, Any]
    ) -> None:
        r"""Receive a scalar "init" event.

        This event is invoked when an uninitialized, unpersisted scalar
        attribute is accessed, e.g. read::


            x = my_object.some_attribute

        The ORM's default behavior when this occurs for an un-initialized
        attribute is to return the value ``None``; note this differs from
        Python's usual behavior of raising ``AttributeError``.    The
        event here can be used to customize what value is actually returned,
        with the assumption that the event listener would be mirroring
        a default generator that is configured on the Core
        :class:`_schema.Column`
        object as well.

        Since a default generator on a :class:`_schema.Column`
        might also produce
        a changing value such as a timestamp, the
        :meth:`.AttributeEvents.init_scalar`
        event handler can also be used to **set** the newly returned value, so
        that a Core-level default generation function effectively fires off
        only once, but at the moment the attribute is accessed on the
        non-persisted object.   Normally, no change to the object's state
        is made when an uninitialized attribute is accessed (much older
        SQLAlchemy versions did in fact change the object's state).

        If a default generator on a column returned a particular constant,
        a handler might be used as follows::

            SOME_CONSTANT = 3.1415926

            class MyClass(Base):
                # ...

                some_attribute = Column(Numeric, default=SOME_CONSTANT)

            @event.listens_for(
                MyClass.some_attribute, "init_scalar",
                retval=True, propagate=True)
            def _init_some_attribute(target, dict_, value):
                dict_['some_attribute'] = SOME_CONSTANT
                return SOME_CONSTANT

        Above, we initialize the attribute ``MyClass.some_attribute`` to the
        value of ``SOME_CONSTANT``.   The above code includes the following
        features:

        * By setting the value ``SOME_CONSTANT`` in the given ``dict_``,
          we indicate that this value is to be persisted to the database.
          This supersedes the use of ``SOME_CONSTANT`` in the default generator
          for the :class:`_schema.Column`.  The ``active_column_defaults.py``
          example given at :ref:`examples_instrumentation` illustrates using
          the same approach for a changing default, e.g. a timestamp
          generator.    In this particular example, it is not strictly
          necessary to do this since ``SOME_CONSTANT`` would be part of the
          INSERT statement in either case.

        * By establishing the ``retval=True`` flag, the value we return
          from the function will be returned by the attribute getter.
          Without this flag, the event is assumed to be a passive observer
          and the return value of our function is ignored.

        * The ``propagate=True`` flag is significant if the mapped class
          includes inheriting subclasses, which would also make use of this
          event listener.  Without this flag, an inheriting subclass will
          not use our event handler.

        In the above example, the attribute set event
        :meth:`.AttributeEvents.set` as well as the related validation feature
        provided by :obj:`_orm.validates` is **not** invoked when we apply our
        value to the given ``dict_``.  To have these events to invoke in
        response to our newly generated value, apply the value to the given
        object as a normal attribute set operation::

            SOME_CONSTANT = 3.1415926

            @event.listens_for(
                MyClass.some_attribute, "init_scalar",
                retval=True, propagate=True)
            def _init_some_attribute(target, dict_, value):
                # will also fire off attribute set events
                target.some_attribute = SOME_CONSTANT
                return SOME_CONSTANT

        When multiple listeners are set up, the generation of the value
        is "chained" from one listener to the next by passing the value
        returned by the previous listener that specifies ``retval=True``
        as the ``value`` argument of the next listener.

        .. versionadded:: 1.1

        :param target: the object instance receiving the event.
         If the listener is registered with ``raw=True``, this will
         be the :class:`.InstanceState` object.
        :param value: the value that is to be returned before this event
         listener were invoked.  This value begins as the value ``None``,
         however will be the return value of the previous event handler
         function if multiple listeners are present.
        :param dict\_: the attribute dictionary of this mapped object.
         This is normally the ``__dict__`` of the object, but in all cases
         represents the destination that the attribute system uses to get
         at the actual value of this attribute.  Placing the value in this
         dictionary has the effect that the value will be used in the
         INSERT statement generated by the unit of work.


        .. seealso::

            :meth:`.AttributeEvents.init_collection` - collection version
            of this event

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.

            :ref:`examples_instrumentation` - see the
            ``active_column_defaults.py`` example.

        """

    def init_collection(
        self,
        target: _O,
        collection: Type[Collection[Any]],
        collection_adapter: CollectionAdapter,
    ) -> None:
        """Receive a 'collection init' event.

        This event is triggered for a collection-based attribute, when
        the initial "empty collection" is first generated for a blank
        attribute, as well as for when the collection is replaced with
        a new one, such as via a set event.

        E.g., given that ``User.addresses`` is a relationship-based
        collection, the event is triggered here::

            u1 = User()
            u1.addresses.append(a1)  #  <- new collection

        and also during replace operations::

            u1.addresses = [a2, a3]  #  <- new collection

        :param target: the object instance receiving the event.
         If the listener is registered with ``raw=True``, this will
         be the :class:`.InstanceState` object.
        :param collection: the new collection.  This will always be generated
         from what was specified as
         :paramref:`_orm.relationship.collection_class`, and will always
         be empty.
        :param collection_adapter: the :class:`.CollectionAdapter` that will
         mediate internal access to the collection.

        .. versionadded:: 1.0.0 :meth:`.AttributeEvents.init_collection`
           and :meth:`.AttributeEvents.dispose_collection` events.

        .. seealso::

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.

            :meth:`.AttributeEvents.init_scalar` - "scalar" version of this
            event.

        """

    def dispose_collection(
        self,
        target: _O,
        collection: Collection[Any],
        collection_adapter: CollectionAdapter,
    ) -> None:
        """Receive a 'collection dispose' event.

        This event is triggered for a collection-based attribute when
        a collection is replaced, that is::

            u1.addresses.append(a1)

            u1.addresses = [a2, a3]  # <- old collection is disposed

        The old collection received will contain its previous contents.

        .. versionchanged:: 1.2 The collection passed to
           :meth:`.AttributeEvents.dispose_collection` will now have its
           contents before the dispose intact; previously, the collection
           would be empty.

        .. versionadded:: 1.0.0 the :meth:`.AttributeEvents.init_collection`
           and :meth:`.AttributeEvents.dispose_collection` events.

        .. seealso::

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.

        """

    def modified(self, target: _O, initiator: Event) -> None:
        """Receive a 'modified' event.

        This event is triggered when the :func:`.attributes.flag_modified`
        function is used to trigger a modify event on an attribute without
        any specific value being set.

        .. versionadded:: 1.2

        :param target: the object instance receiving the event.
          If the listener is registered with ``raw=True``, this will
          be the :class:`.InstanceState` object.

        :param initiator: An instance of :class:`.attributes.Event`
          representing the initiation of the event.

        .. seealso::

            :class:`.AttributeEvents` - background on listener options such
            as propagation to subclasses.

        """


class QueryEvents(event.Events[Query[Any]]):
    """Represent events within the construction of a :class:`_query.Query`
    object.

    .. legacy:: The :class:`_orm.QueryEvents` event methods are legacy
        as of SQLAlchemy 2.0, and only apply to direct use of the
        :class:`_orm.Query` object. They are not used for :term:`2.0 style`
        statements. For events to intercept and modify 2.0 style ORM use,
        use the :meth:`_orm.SessionEvents.do_orm_execute` hook.


    The :class:`_orm.QueryEvents` hooks are now superseded by the
    :meth:`_orm.SessionEvents.do_orm_execute` event hook.

    """

    _target_class_doc = "SomeQuery"
    _dispatch_target = Query

    def before_compile(self, query: Query[Any]) -> None:
        """Receive the :class:`_query.Query`
        object before it is composed into a
        core :class:`_expression.Select` object.

        .. deprecated:: 1.4  The :meth:`_orm.QueryEvents.before_compile` event
           is superseded by the much more capable
           :meth:`_orm.SessionEvents.do_orm_execute` hook.   In version 1.4,
           the :meth:`_orm.QueryEvents.before_compile` event is **no longer
           used** for ORM-level attribute loads, such as loads of deferred
           or expired attributes as well as relationship loaders.   See the
           new examples in :ref:`examples_session_orm_events` which
           illustrate new ways of intercepting and modifying ORM queries
           for the most common purpose of adding arbitrary filter criteria.


        This event is intended to allow changes to the query given::

            @event.listens_for(Query, "before_compile", retval=True)
            def no_deleted(query):
                for desc in query.column_descriptions:
                    if desc['type'] is User:
                        entity = desc['entity']
                        query = query.filter(entity.deleted == False)
                return query

        The event should normally be listened with the ``retval=True``
        parameter set, so that the modified query may be returned.

        The :meth:`.QueryEvents.before_compile` event by default
        will disallow "baked" queries from caching a query, if the event
        hook returns a new :class:`_query.Query` object.
        This affects both direct
        use of the baked query extension as well as its operation within
        lazy loaders and eager loaders for relationships.  In order to
        re-establish the query being cached, apply the event adding the
        ``bake_ok`` flag::

            @event.listens_for(
                Query, "before_compile", retval=True, bake_ok=True)
            def my_event(query):
                for desc in query.column_descriptions:
                    if desc['type'] is User:
                        entity = desc['entity']
                        query = query.filter(entity.deleted == False)
                return query

        When ``bake_ok`` is set to True, the event hook will only be invoked
        once, and not called for subsequent invocations of a particular query
        that is being cached.

        .. versionadded:: 1.3.11  - added the "bake_ok" flag to the
           :meth:`.QueryEvents.before_compile` event and disallowed caching via
           the "baked" extension from occurring for event handlers that
           return  a new :class:`_query.Query` object if this flag is not set.

        .. seealso::

            :meth:`.QueryEvents.before_compile_update`

            :meth:`.QueryEvents.before_compile_delete`

            :ref:`baked_with_before_compile`

        """

    def before_compile_update(
        self, query: Query[Any], update_context: BulkUpdate
    ) -> None:
        """Allow modifications to the :class:`_query.Query` object within
        :meth:`_query.Query.update`.

        .. deprecated:: 1.4  The :meth:`_orm.QueryEvents.before_compile_update`
           event is superseded by the much more capable
           :meth:`_orm.SessionEvents.do_orm_execute` hook.

        Like the :meth:`.QueryEvents.before_compile` event, if the event
        is to be used to alter the :class:`_query.Query` object, it should
        be configured with ``retval=True``, and the modified
        :class:`_query.Query` object returned, as in ::

            @event.listens_for(Query, "before_compile_update", retval=True)
            def no_deleted(query, update_context):
                for desc in query.column_descriptions:
                    if desc['type'] is User:
                        entity = desc['entity']
                        query = query.filter(entity.deleted == False)

                        update_context.values['timestamp'] = datetime.utcnow()
                return query

        The ``.values`` dictionary of the "update context" object can also
        be modified in place as illustrated above.

        :param query: a :class:`_query.Query` instance; this is also
         the ``.query`` attribute of the given "update context"
         object.

        :param update_context: an "update context" object which is
         the same kind of object as described in
         :paramref:`.QueryEvents.after_bulk_update.update_context`.
         The object has a ``.values`` attribute in an UPDATE context which is
         the dictionary of parameters passed to :meth:`_query.Query.update`.
         This
         dictionary can be modified to alter the VALUES clause of the
         resulting UPDATE statement.

        .. versionadded:: 1.2.17

        .. seealso::

            :meth:`.QueryEvents.before_compile`

            :meth:`.QueryEvents.before_compile_delete`


        """

    def before_compile_delete(
        self, query: Query[Any], delete_context: BulkDelete
    ) -> None:
        """Allow modifications to the :class:`_query.Query` object within
        :meth:`_query.Query.delete`.

        .. deprecated:: 1.4  The :meth:`_orm.QueryEvents.before_compile_delete`
           event is superseded by the much more capable
           :meth:`_orm.SessionEvents.do_orm_execute` hook.

        Like the :meth:`.QueryEvents.before_compile` event, this event
        should be configured with ``retval=True``, and the modified
        :class:`_query.Query` object returned, as in ::

            @event.listens_for(Query, "before_compile_delete", retval=True)
            def no_deleted(query, delete_context):
                for desc in query.column_descriptions:
                    if desc['type'] is User:
                        entity = desc['entity']
                        query = query.filter(entity.deleted == False)
                return query

        :param query: a :class:`_query.Query` instance; this is also
         the ``.query`` attribute of the given "delete context"
         object.

        :param delete_context: a "delete context" object which is
         the same kind of object as described in
         :paramref:`.QueryEvents.after_bulk_delete.delete_context`.

        .. versionadded:: 1.2.17

        .. seealso::

            :meth:`.QueryEvents.before_compile`

            :meth:`.QueryEvents.before_compile_update`


        """

    @classmethod
    def _listen(
        cls,
        event_key: _EventKey[_ET],
        retval: bool = False,
        bake_ok: bool = False,
        **kw: Any,
    ) -> None:
        fn = event_key._listen_fn

        if not retval:

            def wrap(*arg: Any, **kw: Any) -> Any:
                if not retval:
                    query = arg[0]
                    fn(*arg, **kw)
                    return query
                else:
                    return fn(*arg, **kw)

            event_key = event_key.with_wrapper(wrap)
        else:
            # don't assume we can apply an attribute to the callable
            def wrap(*arg: Any, **kw: Any) -> Any:
                return fn(*arg, **kw)

            event_key = event_key.with_wrapper(wrap)

        wrap._bake_ok = bake_ok  # type: ignore [attr-defined]

        event_key.base_listen(**kw)

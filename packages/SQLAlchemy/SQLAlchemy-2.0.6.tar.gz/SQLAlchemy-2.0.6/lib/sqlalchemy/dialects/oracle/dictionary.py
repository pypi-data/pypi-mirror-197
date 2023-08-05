# Copyright (C) 2005-2023 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
# mypy: ignore-errors

from .types import DATE
from .types import LONG
from .types import NUMBER
from .types import RAW
from .types import VARCHAR2
from ... import Column
from ... import MetaData
from ... import Table
from ... import table
from ...sql.sqltypes import CHAR

# constants
DB_LINK_PLACEHOLDER = "__$sa_dblink$__"
# tables
dual = table("dual")
dictionary_meta = MetaData()

# NOTE: all the dictionary_meta are aliases because oracle does not like
# using the full table@dblink for every column in query, and complains with
# ORA-00960: ambiguous column naming in select list
all_tables = Table(
    "all_tables" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("tablespace_name", VARCHAR2(30)),
    Column("cluster_name", VARCHAR2(128)),
    Column("iot_name", VARCHAR2(128)),
    Column("status", VARCHAR2(8)),
    Column("pct_free", NUMBER),
    Column("pct_used", NUMBER),
    Column("ini_trans", NUMBER),
    Column("max_trans", NUMBER),
    Column("initial_extent", NUMBER),
    Column("next_extent", NUMBER),
    Column("min_extents", NUMBER),
    Column("max_extents", NUMBER),
    Column("pct_increase", NUMBER),
    Column("freelists", NUMBER),
    Column("freelist_groups", NUMBER),
    Column("logging", VARCHAR2(3)),
    Column("backed_up", VARCHAR2(1)),
    Column("num_rows", NUMBER),
    Column("blocks", NUMBER),
    Column("empty_blocks", NUMBER),
    Column("avg_space", NUMBER),
    Column("chain_cnt", NUMBER),
    Column("avg_row_len", NUMBER),
    Column("avg_space_freelist_blocks", NUMBER),
    Column("num_freelist_blocks", NUMBER),
    Column("degree", VARCHAR2(10)),
    Column("instances", VARCHAR2(10)),
    Column("cache", VARCHAR2(5)),
    Column("table_lock", VARCHAR2(8)),
    Column("sample_size", NUMBER),
    Column("last_analyzed", DATE),
    Column("partitioned", VARCHAR2(3)),
    Column("iot_type", VARCHAR2(12)),
    Column("temporary", VARCHAR2(1)),
    Column("secondary", VARCHAR2(1)),
    Column("nested", VARCHAR2(3)),
    Column("buffer_pool", VARCHAR2(7)),
    Column("flash_cache", VARCHAR2(7)),
    Column("cell_flash_cache", VARCHAR2(7)),
    Column("row_movement", VARCHAR2(8)),
    Column("global_stats", VARCHAR2(3)),
    Column("user_stats", VARCHAR2(3)),
    Column("duration", VARCHAR2(15)),
    Column("skip_corrupt", VARCHAR2(8)),
    Column("monitoring", VARCHAR2(3)),
    Column("cluster_owner", VARCHAR2(128)),
    Column("dependencies", VARCHAR2(8)),
    Column("compression", VARCHAR2(8)),
    Column("compress_for", VARCHAR2(30)),
    Column("dropped", VARCHAR2(3)),
    Column("read_only", VARCHAR2(3)),
    Column("segment_created", VARCHAR2(3)),
    Column("result_cache", VARCHAR2(7)),
    Column("clustering", VARCHAR2(3)),
    Column("activity_tracking", VARCHAR2(23)),
    Column("dml_timestamp", VARCHAR2(25)),
    Column("has_identity", VARCHAR2(3)),
    Column("container_data", VARCHAR2(3)),
    Column("inmemory", VARCHAR2(8)),
    Column("inmemory_priority", VARCHAR2(8)),
    Column("inmemory_distribute", VARCHAR2(15)),
    Column("inmemory_compression", VARCHAR2(17)),
    Column("inmemory_duplicate", VARCHAR2(13)),
    Column("default_collation", VARCHAR2(100)),
    Column("duplicated", VARCHAR2(1)),
    Column("sharded", VARCHAR2(1)),
    Column("externally_sharded", VARCHAR2(1)),
    Column("externally_duplicated", VARCHAR2(1)),
    Column("external", VARCHAR2(3)),
    Column("hybrid", VARCHAR2(3)),
    Column("cellmemory", VARCHAR2(24)),
    Column("containers_default", VARCHAR2(3)),
    Column("container_map", VARCHAR2(3)),
    Column("extended_data_link", VARCHAR2(3)),
    Column("extended_data_link_map", VARCHAR2(3)),
    Column("inmemory_service", VARCHAR2(12)),
    Column("inmemory_service_name", VARCHAR2(1000)),
    Column("container_map_object", VARCHAR2(3)),
    Column("memoptimize_read", VARCHAR2(8)),
    Column("memoptimize_write", VARCHAR2(8)),
    Column("has_sensitive_column", VARCHAR2(3)),
    Column("admit_null", VARCHAR2(3)),
    Column("data_link_dml_enabled", VARCHAR2(3)),
    Column("logical_replication", VARCHAR2(8)),
).alias("a_tables")

all_views = Table(
    "all_views" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("view_name", VARCHAR2(128), nullable=False),
    Column("text_length", NUMBER),
    Column("text", LONG),
    Column("text_vc", VARCHAR2(4000)),
    Column("type_text_length", NUMBER),
    Column("type_text", VARCHAR2(4000)),
    Column("oid_text_length", NUMBER),
    Column("oid_text", VARCHAR2(4000)),
    Column("view_type_owner", VARCHAR2(128)),
    Column("view_type", VARCHAR2(128)),
    Column("superview_name", VARCHAR2(128)),
    Column("editioning_view", VARCHAR2(1)),
    Column("read_only", VARCHAR2(1)),
    Column("container_data", VARCHAR2(1)),
    Column("bequeath", VARCHAR2(12)),
    Column("origin_con_id", VARCHAR2(256)),
    Column("default_collation", VARCHAR2(100)),
    Column("containers_default", VARCHAR2(3)),
    Column("container_map", VARCHAR2(3)),
    Column("extended_data_link", VARCHAR2(3)),
    Column("extended_data_link_map", VARCHAR2(3)),
    Column("has_sensitive_column", VARCHAR2(3)),
    Column("admit_null", VARCHAR2(3)),
    Column("pdb_local_only", VARCHAR2(3)),
).alias("a_views")

all_sequences = Table(
    "all_sequences" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("sequence_owner", VARCHAR2(128), nullable=False),
    Column("sequence_name", VARCHAR2(128), nullable=False),
    Column("min_value", NUMBER),
    Column("max_value", NUMBER),
    Column("increment_by", NUMBER, nullable=False),
    Column("cycle_flag", VARCHAR2(1)),
    Column("order_flag", VARCHAR2(1)),
    Column("cache_size", NUMBER, nullable=False),
    Column("last_number", NUMBER, nullable=False),
    Column("scale_flag", VARCHAR2(1)),
    Column("extend_flag", VARCHAR2(1)),
    Column("sharded_flag", VARCHAR2(1)),
    Column("session_flag", VARCHAR2(1)),
    Column("keep_value", VARCHAR2(1)),
).alias("a_sequences")

all_users = Table(
    "all_users" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("username", VARCHAR2(128), nullable=False),
    Column("user_id", NUMBER, nullable=False),
    Column("created", DATE, nullable=False),
    Column("common", VARCHAR2(3)),
    Column("oracle_maintained", VARCHAR2(1)),
    Column("inherited", VARCHAR2(3)),
    Column("default_collation", VARCHAR2(100)),
    Column("implicit", VARCHAR2(3)),
    Column("all_shard", VARCHAR2(3)),
    Column("external_shard", VARCHAR2(3)),
).alias("a_users")

all_mviews = Table(
    "all_mviews" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("mview_name", VARCHAR2(128), nullable=False),
    Column("container_name", VARCHAR2(128), nullable=False),
    Column("query", LONG),
    Column("query_len", NUMBER(38)),
    Column("updatable", VARCHAR2(1)),
    Column("update_log", VARCHAR2(128)),
    Column("master_rollback_seg", VARCHAR2(128)),
    Column("master_link", VARCHAR2(128)),
    Column("rewrite_enabled", VARCHAR2(1)),
    Column("rewrite_capability", VARCHAR2(9)),
    Column("refresh_mode", VARCHAR2(6)),
    Column("refresh_method", VARCHAR2(8)),
    Column("build_mode", VARCHAR2(9)),
    Column("fast_refreshable", VARCHAR2(18)),
    Column("last_refresh_type", VARCHAR2(8)),
    Column("last_refresh_date", DATE),
    Column("last_refresh_end_time", DATE),
    Column("staleness", VARCHAR2(19)),
    Column("after_fast_refresh", VARCHAR2(19)),
    Column("unknown_prebuilt", VARCHAR2(1)),
    Column("unknown_plsql_func", VARCHAR2(1)),
    Column("unknown_external_table", VARCHAR2(1)),
    Column("unknown_consider_fresh", VARCHAR2(1)),
    Column("unknown_import", VARCHAR2(1)),
    Column("unknown_trusted_fd", VARCHAR2(1)),
    Column("compile_state", VARCHAR2(19)),
    Column("use_no_index", VARCHAR2(1)),
    Column("stale_since", DATE),
    Column("num_pct_tables", NUMBER),
    Column("num_fresh_pct_regions", NUMBER),
    Column("num_stale_pct_regions", NUMBER),
    Column("segment_created", VARCHAR2(3)),
    Column("evaluation_edition", VARCHAR2(128)),
    Column("unusable_before", VARCHAR2(128)),
    Column("unusable_beginning", VARCHAR2(128)),
    Column("default_collation", VARCHAR2(100)),
    Column("on_query_computation", VARCHAR2(1)),
    Column("auto", VARCHAR2(3)),
).alias("a_mviews")

all_tab_identity_cols = Table(
    "all_tab_identity_cols" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("column_name", VARCHAR2(128), nullable=False),
    Column("generation_type", VARCHAR2(10)),
    Column("sequence_name", VARCHAR2(128), nullable=False),
    Column("identity_options", VARCHAR2(298)),
).alias("a_tab_identity_cols")

all_tab_cols = Table(
    "all_tab_cols" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("column_name", VARCHAR2(128), nullable=False),
    Column("data_type", VARCHAR2(128)),
    Column("data_type_mod", VARCHAR2(3)),
    Column("data_type_owner", VARCHAR2(128)),
    Column("data_length", NUMBER, nullable=False),
    Column("data_precision", NUMBER),
    Column("data_scale", NUMBER),
    Column("nullable", VARCHAR2(1)),
    Column("column_id", NUMBER),
    Column("default_length", NUMBER),
    Column("data_default", LONG),
    Column("num_distinct", NUMBER),
    Column("low_value", RAW(1000)),
    Column("high_value", RAW(1000)),
    Column("density", NUMBER),
    Column("num_nulls", NUMBER),
    Column("num_buckets", NUMBER),
    Column("last_analyzed", DATE),
    Column("sample_size", NUMBER),
    Column("character_set_name", VARCHAR2(44)),
    Column("char_col_decl_length", NUMBER),
    Column("global_stats", VARCHAR2(3)),
    Column("user_stats", VARCHAR2(3)),
    Column("avg_col_len", NUMBER),
    Column("char_length", NUMBER),
    Column("char_used", VARCHAR2(1)),
    Column("v80_fmt_image", VARCHAR2(3)),
    Column("data_upgraded", VARCHAR2(3)),
    Column("hidden_column", VARCHAR2(3)),
    Column("virtual_column", VARCHAR2(3)),
    Column("segment_column_id", NUMBER),
    Column("internal_column_id", NUMBER, nullable=False),
    Column("histogram", VARCHAR2(15)),
    Column("qualified_col_name", VARCHAR2(4000)),
    Column("user_generated", VARCHAR2(3)),
    Column("default_on_null", VARCHAR2(3)),
    Column("identity_column", VARCHAR2(3)),
    Column("evaluation_edition", VARCHAR2(128)),
    Column("unusable_before", VARCHAR2(128)),
    Column("unusable_beginning", VARCHAR2(128)),
    Column("collation", VARCHAR2(100)),
    Column("collated_column_id", NUMBER),
).alias("a_tab_cols")

all_tab_comments = Table(
    "all_tab_comments" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("table_type", VARCHAR2(11)),
    Column("comments", VARCHAR2(4000)),
    Column("origin_con_id", NUMBER),
).alias("a_tab_comments")

all_col_comments = Table(
    "all_col_comments" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("column_name", VARCHAR2(128), nullable=False),
    Column("comments", VARCHAR2(4000)),
    Column("origin_con_id", NUMBER),
).alias("a_col_comments")

all_mview_comments = Table(
    "all_mview_comments" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("mview_name", VARCHAR2(128), nullable=False),
    Column("comments", VARCHAR2(4000)),
).alias("a_mview_comments")

all_ind_columns = Table(
    "all_ind_columns" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("index_owner", VARCHAR2(128), nullable=False),
    Column("index_name", VARCHAR2(128), nullable=False),
    Column("table_owner", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("column_name", VARCHAR2(4000)),
    Column("column_position", NUMBER, nullable=False),
    Column("column_length", NUMBER, nullable=False),
    Column("char_length", NUMBER),
    Column("descend", VARCHAR2(4)),
    Column("collated_column_id", NUMBER),
).alias("a_ind_columns")

all_indexes = Table(
    "all_indexes" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("index_name", VARCHAR2(128), nullable=False),
    Column("index_type", VARCHAR2(27)),
    Column("table_owner", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("table_type", CHAR(11)),
    Column("uniqueness", VARCHAR2(9)),
    Column("compression", VARCHAR2(13)),
    Column("prefix_length", NUMBER),
    Column("tablespace_name", VARCHAR2(30)),
    Column("ini_trans", NUMBER),
    Column("max_trans", NUMBER),
    Column("initial_extent", NUMBER),
    Column("next_extent", NUMBER),
    Column("min_extents", NUMBER),
    Column("max_extents", NUMBER),
    Column("pct_increase", NUMBER),
    Column("pct_threshold", NUMBER),
    Column("include_column", NUMBER),
    Column("freelists", NUMBER),
    Column("freelist_groups", NUMBER),
    Column("pct_free", NUMBER),
    Column("logging", VARCHAR2(3)),
    Column("blevel", NUMBER),
    Column("leaf_blocks", NUMBER),
    Column("distinct_keys", NUMBER),
    Column("avg_leaf_blocks_per_key", NUMBER),
    Column("avg_data_blocks_per_key", NUMBER),
    Column("clustering_factor", NUMBER),
    Column("status", VARCHAR2(8)),
    Column("num_rows", NUMBER),
    Column("sample_size", NUMBER),
    Column("last_analyzed", DATE),
    Column("degree", VARCHAR2(40)),
    Column("instances", VARCHAR2(40)),
    Column("partitioned", VARCHAR2(3)),
    Column("temporary", VARCHAR2(1)),
    Column("generated", VARCHAR2(1)),
    Column("secondary", VARCHAR2(1)),
    Column("buffer_pool", VARCHAR2(7)),
    Column("flash_cache", VARCHAR2(7)),
    Column("cell_flash_cache", VARCHAR2(7)),
    Column("user_stats", VARCHAR2(3)),
    Column("duration", VARCHAR2(15)),
    Column("pct_direct_access", NUMBER),
    Column("ityp_owner", VARCHAR2(128)),
    Column("ityp_name", VARCHAR2(128)),
    Column("parameters", VARCHAR2(1000)),
    Column("global_stats", VARCHAR2(3)),
    Column("domidx_status", VARCHAR2(12)),
    Column("domidx_opstatus", VARCHAR2(6)),
    Column("funcidx_status", VARCHAR2(8)),
    Column("join_index", VARCHAR2(3)),
    Column("iot_redundant_pkey_elim", VARCHAR2(3)),
    Column("dropped", VARCHAR2(3)),
    Column("visibility", VARCHAR2(9)),
    Column("domidx_management", VARCHAR2(14)),
    Column("segment_created", VARCHAR2(3)),
    Column("orphaned_entries", VARCHAR2(3)),
    Column("indexing", VARCHAR2(7)),
    Column("auto", VARCHAR2(3)),
).alias("a_indexes")

all_constraints = Table(
    "all_constraints" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128)),
    Column("constraint_name", VARCHAR2(128)),
    Column("constraint_type", VARCHAR2(1)),
    Column("table_name", VARCHAR2(128)),
    Column("search_condition", LONG),
    Column("search_condition_vc", VARCHAR2(4000)),
    Column("r_owner", VARCHAR2(128)),
    Column("r_constraint_name", VARCHAR2(128)),
    Column("delete_rule", VARCHAR2(9)),
    Column("status", VARCHAR2(8)),
    Column("deferrable", VARCHAR2(14)),
    Column("deferred", VARCHAR2(9)),
    Column("validated", VARCHAR2(13)),
    Column("generated", VARCHAR2(14)),
    Column("bad", VARCHAR2(3)),
    Column("rely", VARCHAR2(4)),
    Column("last_change", DATE),
    Column("index_owner", VARCHAR2(128)),
    Column("index_name", VARCHAR2(128)),
    Column("invalid", VARCHAR2(7)),
    Column("view_related", VARCHAR2(14)),
    Column("origin_con_id", VARCHAR2(256)),
).alias("a_constraints")

all_cons_columns = Table(
    "all_cons_columns" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("constraint_name", VARCHAR2(128), nullable=False),
    Column("table_name", VARCHAR2(128), nullable=False),
    Column("column_name", VARCHAR2(4000)),
    Column("position", NUMBER),
).alias("a_cons_columns")

# TODO figure out if it's still relevant, since there is no mention from here
# https://docs.oracle.com/en/database/oracle/oracle-database/21/refrn/ALL_DB_LINKS.html
# original note:
# using user_db_links here since all_db_links appears
# to have more restricted permissions.
# https://docs.oracle.com/cd/B28359_01/server.111/b28310/ds_admin005.htm
# will need to hear from more users if we are doing
# the right thing here.  See [ticket:2619]
all_db_links = Table(
    "all_db_links" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("db_link", VARCHAR2(128), nullable=False),
    Column("username", VARCHAR2(128)),
    Column("host", VARCHAR2(2000)),
    Column("created", DATE, nullable=False),
    Column("hidden", VARCHAR2(3)),
    Column("shard_internal", VARCHAR2(3)),
    Column("valid", VARCHAR2(3)),
    Column("intra_cdb", VARCHAR2(3)),
).alias("a_db_links")

all_synonyms = Table(
    "all_synonyms" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128)),
    Column("synonym_name", VARCHAR2(128)),
    Column("table_owner", VARCHAR2(128)),
    Column("table_name", VARCHAR2(128)),
    Column("db_link", VARCHAR2(128)),
    Column("origin_con_id", VARCHAR2(256)),
).alias("a_synonyms")

all_objects = Table(
    "all_objects" + DB_LINK_PLACEHOLDER,
    dictionary_meta,
    Column("owner", VARCHAR2(128), nullable=False),
    Column("object_name", VARCHAR2(128), nullable=False),
    Column("subobject_name", VARCHAR2(128)),
    Column("object_id", NUMBER, nullable=False),
    Column("data_object_id", NUMBER),
    Column("object_type", VARCHAR2(23)),
    Column("created", DATE, nullable=False),
    Column("last_ddl_time", DATE, nullable=False),
    Column("timestamp", VARCHAR2(19)),
    Column("status", VARCHAR2(7)),
    Column("temporary", VARCHAR2(1)),
    Column("generated", VARCHAR2(1)),
    Column("secondary", VARCHAR2(1)),
    Column("namespace", NUMBER, nullable=False),
    Column("edition_name", VARCHAR2(128)),
    Column("sharing", VARCHAR2(13)),
    Column("editionable", VARCHAR2(1)),
    Column("oracle_maintained", VARCHAR2(1)),
    Column("application", VARCHAR2(1)),
    Column("default_collation", VARCHAR2(100)),
    Column("duplicated", VARCHAR2(1)),
    Column("sharded", VARCHAR2(1)),
    Column("created_appid", NUMBER),
    Column("created_vsnid", NUMBER),
    Column("modified_appid", NUMBER),
    Column("modified_vsnid", NUMBER),
).alias("a_objects")

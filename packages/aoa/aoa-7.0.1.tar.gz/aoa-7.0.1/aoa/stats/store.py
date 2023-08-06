import json
import pandas as pd
from typing import Dict
import logging

from teradataml import (
    get_connection
)

logger = logging.getLogger(__name__)

ct_query = """
CT {} (
    column_name VARCHAR(128), 
    column_type VARCHAR(128),
    stats JSON, 
    update_ts TIMESTAMP)
UNIQUE PRIMARY INDEX ( column_name );
"""

merge_query = """
MERGE {} target
     USING {} source
       ON target.column_name = source.column_name
     WHEN MATCHED THEN
       UPD SET stats = source.stats, column_type = source.column_type, update_ts = source.update_ts
     WHEN NOT MATCHED THEN
       INS (source.column_name, source.column_type, source.stats, source.update_ts);
"""
temp_table = "aoa_stats_temp"


def save_feature_stats(features_table: str, feature_type: str, stats: Dict) -> None:
    cvt_query = f"CREATE VOLATILE TABLE {temp_table} AS {features_table} WITH NO DATA ON COMMIT PRESERVE ROWS;"
    ins_query = f"INS {temp_table} (column_name,column_type,stats,update_ts) VALUES(?,?,?,CURRENT_TIMESTAMP);"
    m_query = merge_query.format(features_table, temp_table)
    dt_query = f"DROP TABLE {temp_table};"

    conn = get_connection()
    logging.debug(cvt_query)
    conn.execute(cvt_query)
    logging.debug(ins_query)
    conn.execute(ins_query, [[f, feature_type, json.dumps(stats[f])] for f in stats])
    logging.debug(m_query)
    conn.execute(m_query)
    logging.debug(dt_query)
    conn.execute(dt_query)


def get_feature_stats_summary(features_table: str) -> Dict:
    fs = pd.read_sql(f"SEL column_name, column_type FROM {features_table} ORDER BY column_type", get_connection())
    fs = fs.reset_index().drop(fs.columns.difference(["column_name", "column_type"]), axis=1)
    fs = fs.set_index("column_name")
    return pd.Series(fs.column_type).to_dict()


def get_feature_stats(features_table: str, feature_type: str) -> Dict:
    fs = pd.read_sql(f"SEL * FROM {features_table} WHERE column_type='{feature_type}'", get_connection())
    fs = fs.reset_index().drop(fs.columns.difference(["column_name", "stats"]), axis=1)
    fs = fs.set_index("column_name")
    fs = pd.Series(fs.stats).to_dict()
    return {k: json.loads(fs[k]) for k in fs}


def create_features_stats_table(features_table: str) -> None:
    conn = get_connection()
    query = ct_query.format(features_table)
    logging.debug(query)
    conn.execute(query)

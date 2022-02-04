# -*- coding: utf-8 -*-

DEFAULT_CHUNK_TIME_INTERVAL_DAYS = 1
DEFAULT_RETENTION_DAYS = 90

_CREATE_HYPERTABLE_FORMAT = """
SELECT
    create_hypertable(
        '{table}',
        '{column}',
        chunk_time_interval => INTERVAL '{chunk_time_interval_days} days'
    )
WHERE
    NOT EXISTS(
        SELECT *
        FROM timescaledb_information.hypertables
        WHERE hypertable_name='{table}'
    );
"""

_ADD_RETENTION_POLICY_FORMAT = """
SELECT
    add_retention_policy(
        '{table}',
        INTERVAL '{retention_days} days'
    )
WHERE
    NOT EXISTS(
        SELECT *
        FROM timescaledb_information.jobs
        WHERE
            proc_name='policy_retention'
            AND hypertable_name='{table}'
    );
"""


def get_create_hypertable_format(
    table: str,
    column: str,
    chunk_time_interval_days=DEFAULT_CHUNK_TIME_INTERVAL_DAYS,
) -> str:
    return _CREATE_HYPERTABLE_FORMAT.format(
        table=table,
        column=column,
        chunk_time_interval_days=chunk_time_interval_days,
    )


def get_add_retention_policy_format(
    table: str,
    retention_days=DEFAULT_RETENTION_DAYS,
) -> str:
    return _ADD_RETENTION_POLICY_FORMAT.format(
        table=table,
        retention_days=retention_days,
    )

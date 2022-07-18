# -*- coding: utf-8 -*-

from datetime import datetime
from functools import reduce
from typing import List

from recc.packet.port import SockType
from recc.variables.database import (
    DAEMON_NAME_STR_SIZE,
    DAEMON_PLUGIN_STR_SIZE,
    DAEMON_SLUG_STR_SIZE,
    FUNC_ADD_DAEMON_AND_PORT,
    REFERENCE_CATEGORY_RECC_DAEMON,
    TABLE_DAEMON,
    TABLE_PORT,
    URL_STR_SIZE,
)

CREATE_FUNC_ADD_DAEMON_AND_PORT = f"""
CREATE OR REPLACE FUNCTION {FUNC_ADD_DAEMON_AND_PORT} (
    d_plugin VARCHAR({DAEMON_PLUGIN_STR_SIZE}),
    d_slug VARCHAR({DAEMON_SLUG_STR_SIZE}),
    d_name VARCHAR({DAEMON_NAME_STR_SIZE}),
    d_address VARCHAR({URL_STR_SIZE}),
    d_description TEXT,
    d_enable BOOLEAN,
    d_created TIMESTAMPTZ,
    p_tcp_ports INTEGER[]
)
    RETURNS INTEGER
    LANGUAGE plpgsql
AS $function$
DECLARE
    r_uid INTEGER;
    tcp_port INTEGER;
BEGIN
    INSERT INTO {TABLE_DAEMON} (
        plugin,
        slug,
        name,
        address,
        description,
        enable,
        created_at,
        updated_at
    ) VALUES (
        d_plugin,
        d_slug,
        d_name,
        d_address,
        d_description,
        d_enable,
        d_created,
        d_created
    ) RETURNING uid INTO r_uid;

    FOREACH tcp_port IN ARRAY p_tcp_ports LOOP
        INSERT INTO {TABLE_PORT} (
            number,
            sock,
            ref_uid,
            ref_category,
            created_at,
            updated_at
        ) VALUES (
            tcp_port,
            {SockType.Stream.value},
            r_uid,
            '{REFERENCE_CATEGORY_RECC_DAEMON}',
            d_created,
            d_created
        );
    END LOOP;

    RETURN r_uid;
END;
$function$;
"""

DROP_FUNC_ADD_DAEMON_AND_PORT = f"""
DROP FUNCTION IF EXISTS {FUNC_ADD_DAEMON_AND_PORT};
"""

_INSERT_DAEMON_AND_PORT = f"""
SELECT * FROM {FUNC_ADD_DAEMON_AND_PORT}(
    '{{d_plugin}}',
    '{{d_slug}}',
    '{{d_name}}',
    '{{d_address}}',
    '{{d_description}}',
    {{d_enable}},
    TIMESTAMPTZ '{{d_created}}',
    ARRAY[{{p_tcp_ports}}]::INTEGER[]
)
"""


def get_insert_daemon_and_port(
    d_plugin: str,
    d_slug: str,
    d_name: str,
    d_address: str,
    d_description: str,
    d_enable: bool,
    d_created: datetime,
    p_tcp_ports: List[int],
) -> str:
    assert d_created.tzinfo is not None
    if p_tcp_ports:
        tcp_ports = reduce(lambda x, y: f"{x},{y}", map(lambda x: str(x), p_tcp_ports))
    else:
        tcp_ports = str()
    return _INSERT_DAEMON_AND_PORT.format(
        d_plugin=d_plugin,
        d_slug=d_slug,
        d_name=d_name,
        d_address=d_address,
        d_description=d_description,
        d_enable="TRUE" if d_enable else "FALSE",
        d_created=d_created.isoformat(),
        p_tcp_ports=tcp_ports,
    )

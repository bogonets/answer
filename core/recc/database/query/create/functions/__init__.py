# -*- coding: utf-8 -*-

from recc.database.query.create.functions.add_daemon_and_port import (
    CREATE_FUNC_ADD_DAEMON_AND_PORT,
    DROP_FUNC_ADD_DAEMON_AND_PORT,
)
from recc.database.query.create.functions.appropriate_permission import (
    CREATE_FUNC_APPROPRIATE_PERMISSION,
    DROP_FUNC_APPROPRIATE_PERMISSION,
)

CREATE_FUNCTIONS = (
    CREATE_FUNC_APPROPRIATE_PERMISSION,
    CREATE_FUNC_ADD_DAEMON_AND_PORT,
)

DROP_FUNCTIONS = (
    DROP_FUNC_APPROPRIATE_PERMISSION,
    DROP_FUNC_ADD_DAEMON_AND_PORT,
)

__all__ = ("CREATE_FUNCTIONS", "DROP_FUNCTIONS")

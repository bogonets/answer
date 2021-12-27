# -*- coding: utf-8 -*-

from recc.variables.database import VIEW_UNION_MEMBER

SELECT_UNION_MEMBER_ALL = f"""
SELECT *
FROM {VIEW_UNION_MEMBER};
"""

SELECT_UNION_MEMBER_BY_USER = f"""
SELECT *
FROM {VIEW_UNION_MEMBER}
WHERE user_uid=$1;
"""

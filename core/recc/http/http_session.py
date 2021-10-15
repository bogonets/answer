# -*- coding: utf-8 -*-

from aiohttp.web_request import Request
from aiohttp.hdrs import AUTHORIZATION
from recc.core.context import Context
from recc.session.session_ex import SessionEx
from recc.http.header.bearer_auth import BearerAuth
from recc.http import http_cache_keys as c


async def assign_session(context: Context, request: Request) -> None:
    authorization = request.headers[AUTHORIZATION]
    bearer = BearerAuth.decode_from_authorization_header(authorization)
    session = await context.get_access_session(bearer.token)
    audience_uid = await context.get_user_uid(session.audience)
    db_user = await context.get_user(audience_uid)
    request[c.context] = context
    request[c.session] = SessionEx(
        session,
        audience_uid,
        True if db_user.is_admin else False,
        db_user.extra,
    )

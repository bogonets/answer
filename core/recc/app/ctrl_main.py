# -*- coding: utf-8 -*-

import asyncio
from typing import List
from http import HTTPStatus
from recc.argparse.config.ctrl_config import CtrlConfig
from recc.http.http_client import HttpClient
from recc.http.http_utils import v2_admin_path
from recc.http import http_urls as u
from recc.packet.info import InfoA, CreateInfoQ, UpdateInfoQ


async def ctrl_main_runner(config: CtrlConfig) -> int:
    scheme = config.scheme
    address = config.address
    timeout = config.timeout
    client = HttpClient(address, timeout=timeout, scheme=scheme)

    print(f"Origin: {client.origin}")

    username = config.username
    password = config.password
    print(f"username: {username}")
    print(f"password: {password}")

    if username:
        await client.signin(username, password, save_session=True)

    print(f"ctrl_main: {config.unrecognized_arguments}")

    category = config.unrecognized_arguments[0]
    if category == "admin":
        subcategory = config.unrecognized_arguments[1]
        if subcategory == "infos":
            action = config.unrecognized_arguments[2]

            if action == "list":
                response = await client.get(v2_admin_path(u.infos), cls=List[InfoA])
                if response.status == HTTPStatus.OK:
                    assert isinstance(response.data, list)
                    print(response.data)
                else:
                    print(f"[{response.status}] {response.reason}")
            elif action == "get":
                key = config.unrecognized_arguments[3]
                path = v2_admin_path(u.infos_pkey, key=key)
                response = await client.get(path, cls=InfoA)
                exists_info = response.status == HTTPStatus.OK

                if exists_info:
                    assert isinstance(response.data, InfoA)
                    print(response.data.value)
                else:
                    print(f"[{response.status}] {response.reason}")
            elif action == "set":
                key = config.unrecognized_arguments[3]
                value = config.unrecognized_arguments[4]
                path = v2_admin_path(u.infos_pkey, key=key)
                response = await client.get(path, cls=InfoA)
                exists_info = response.status == HTTPStatus.OK
                if exists_info:
                    await client.patch(path, data=UpdateInfoQ(value))
                else:
                    await client.post(
                        v2_admin_path(u.infos),
                        data=CreateInfoQ(key, value),
                    )
            elif action == "del":
                key = config.unrecognized_arguments[3]
                path = v2_admin_path(u.infos_pkey, key=key)
                await client.delete(path)

    return 0


def ctrl_main(config: CtrlConfig) -> int:
    return asyncio.run(ctrl_main_runner(config))

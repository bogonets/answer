# -*- coding: utf-8 -*-

from recc.argparse.config.ctrl_config import CtrlConfig


def ctrl_main(config: CtrlConfig) -> int:
    print(f"ctrl_main: {config.unrecognized_arguments}")
    category = config.unrecognized_arguments[0]
    if category == "admin":
        subcategory = config.unrecognized_arguments[1]
        if subcategory == "infos":
            action = config.unrecognized_arguments[2]
            if action == "set":
                # key = config.unrecognized_arguments[3]
                # val = config.unrecognized_arguments[4]
                # prefix = f"{config.scheme}://{config.address}"
                # path = v2_admin_path(u.infos_pkey.format(key=key))
                #
                # if prefix[-1] == URL_PATH_SEPARATOR:
                #     url = prefix[0:-1] + path
                # else:
                #     url = prefix + path
                #
                # request_body = global_json_encoder(serialize_default(val))
                # headers = CIMultiDict[str]()
                # if CONTENT_TYPE not in headers:
                #     headers.add(CONTENT_TYPE, str(MIME_APPLICATION_JSON_UTF8))
                # cls = InfoA
                #
                # async with ClientSession(timeout=config.timeout) as session:
                #     method_caller = get_method_caller(METH_POST, session)
                #     async with method_caller(
                #         url=url, data=request_body, headers=headers
                #     ) as response:
                #         response_data: Any = None
                #         if cls is not None:
                #             response_data = payload_to_class(
                #                 response.headers, await response.text(), cls
                #             )
                #         elif response.content_length > 0:
                #             if response.content_type == APPLICATION_JSON:
                #                 response_data = await response.json()
                #             else:
                #                 response_data = await response.text()
                pass

    return 0

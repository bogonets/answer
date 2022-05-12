# -*- coding: utf-8 -*-

from aiohttp import web
from aiohttp_cors import CorsConfig, ResourceOptions, setup


def create_cors(app: web.Application) -> CorsConfig:
    cors = setup(
        app,
        defaults={
            "*": ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                max_age=None,
                allow_methods=None,
            )
        },
    )

    routes = list(app.router.routes())
    for route in routes:
        cors.add(route)
    return cors

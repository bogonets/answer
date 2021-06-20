# -*- coding: utf-8 -*-

import os
import time
from typing import Optional
from elasticsearch import AsyncElasticsearch

DEFAULT_ELASTICSEARCH_INDEX_NAME = "answer"
DEFAULT_ELASTICSEARCH_HOST = "localhost"
DEFAULT_ELASTICSEARCH_PORT = 9200

DEFAULT_ELASTICSEARCH_PROP_NAME = "name"
DEFAULT_ELASTICSEARCH_PROP_PID = "pid"
DEFAULT_ELASTICSEARCH_PROP_TIME = "time"
DEFAULT_ELASTICSEARCH_PROP_LEVEL = "level"
DEFAULT_ELASTICSEARCH_PROP_MSG = "msg"

DEFAULT_ELASTICSEARCH_MAPPING = {
    "mappings": {
        "properties": {
            DEFAULT_ELASTICSEARCH_PROP_NAME: {
                "type": "keyword",
            },
            DEFAULT_ELASTICSEARCH_PROP_PID: {
                "type": "integer",
            },
            DEFAULT_ELASTICSEARCH_PROP_TIME: {
                "type": "date",
                "format": "epoch_millis",
            },
            DEFAULT_ELASTICSEARCH_PROP_LEVEL: {
                "type": "short",
            },
            DEFAULT_ELASTICSEARCH_PROP_MSG: {
                "type": "text",
            },
        },
    },
}


class AsyncElasticLogger:
    def __init__(
        self,
        name: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        index: Optional[str] = None,
    ):
        self.name = name
        self.host = host if host else DEFAULT_ELASTICSEARCH_HOST
        self.port = port if port else DEFAULT_ELASTICSEARCH_PORT
        self.index = index if index else DEFAULT_ELASTICSEARCH_INDEX_NAME

        self._pid = os.getpid()
        self._mapping = DEFAULT_ELASTICSEARCH_MAPPING
        self._ready = False
        self._es = AsyncElasticsearch(f"{self.host}:{self.port}")

    async def open(self) -> bool:
        try:
            if not await self._es.indices.exists(index=self.index):
                await self._es.indices.create(index=self.index, body=self._mapping)
            self._ready = True
            return True
        except Exception:  # noqa
            self._ready = False
            return False

    async def close(self) -> None:
        if self._ready:
            try:
                await self._es.close()
            except Exception:  # noqa
                pass
            finally:
                self._ready = False

    async def write(self, level: int, msg: str):
        return await self._es.index(
            index=self.index,
            doc_type="_doc",
            body={
                DEFAULT_ELASTICSEARCH_PROP_NAME: self.name,
                DEFAULT_ELASTICSEARCH_PROP_PID: self._pid,
                DEFAULT_ELASTICSEARCH_PROP_TIME: int(time.time() * 1000),
                DEFAULT_ELASTICSEARCH_PROP_LEVEL: level,
                DEFAULT_ELASTICSEARCH_PROP_MSG: msg,
            },
        )

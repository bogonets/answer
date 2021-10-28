# -*- coding: utf-8 -*-

from typing import Optional, Dict, Set, List, Any, Union, Callable, Awaitable
from asyncio import Task, create_task, TimeoutError
from overrides import overrides
from aioredis import Redis, ConnectionPool
from aioredis.client import PubSub
from inspect import iscoroutinefunction, isfunction
from async_timeout import timeout as async_timeout_timeout
from recc.cache.cache_store_interface import CacheStoreInterface
from recc.variables.cache import DEFAULT_MAX_CONNECTIONS

EX_KEY_MAX_CONNECTIONS = "max_connections"

SubscribeAsyncCallable = Callable[[Any], Awaitable[None]]
SubscribeSyncCallable = Callable[[Any], None]
SubscribeCallable = Union[SubscribeAsyncCallable, SubscribeSyncCallable]


class RedisCacheStore(CacheStoreInterface):
    """
    Redis cache store class.
    """

    def __init__(
        self,
        cs_host: str,
        cs_port: int,
        cs_pw: Optional[str] = None,
        **kwargs,
    ):
        self._cs_host = cs_host
        self._cs_port = cs_port
        self._cs_pw = cs_pw
        self._kwargs = kwargs
        self._redis: Optional[Redis] = None

        self._subscribes: Dict[str, Task] = dict()
        self._subscribes_tick = 1.0
        self._subscribes_exit: Set[str] = set()
        self._subscribes_close_timeout = 5.0

    def _get_max_connections(self, default_value=DEFAULT_MAX_CONNECTIONS) -> int:
        try:
            return int(self._kwargs.get(EX_KEY_MAX_CONNECTIONS, default_value))
        except ValueError:
            return default_value

    @overrides
    def is_open(self) -> bool:
        return self._redis is not None

    @overrides
    async def open(self) -> None:
        pool = ConnectionPool.from_url(
            f"redis://{self._cs_host}:{self._cs_port}",
            password=self._cs_pw if self._cs_pw else None,
            max_connections=self._get_max_connections(),
        )
        self._redis = Redis(connection_pool=pool)

    async def close_subscribes(self) -> None:
        try:
            for channel in self._subscribes.keys():
                self._subscribes_exit.add(channel)
            async with async_timeout_timeout(self._subscribes_close_timeout):
                for task in self._subscribes.values():
                    await task
        except TimeoutError:
            for task in self._subscribes.values():
                task.cancel()
        finally:
            self._subscribes.clear()
            self._subscribes_exit.clear()

    @overrides
    async def close(self) -> None:
        assert self._redis
        await self.close_subscribes()
        assert len(self._subscribes) == 0
        await self._redis.close()
        self._redis = None

    @property
    def redis(self) -> Redis:
        assert self._redis is not None
        return self._redis

    @overrides
    async def set(self, key: str, val: bytes) -> None:
        await self.redis.execute_command("SET", key, val)

    @overrides
    async def get(self, key: str) -> bytes:
        result = await self.redis.execute_command("GET", key)
        assert isinstance(result, bytes)
        return result

    @overrides
    async def delete(self, key: str) -> None:
        await self.redis.execute_command("DEL", key)

    @overrides
    async def exists(self, key: str) -> bool:
        result = await self.redis.execute_command("EXISTS", key)
        assert isinstance(result, int)
        return bool(result)

    async def _subscribe_task(
        self,
        key: str,
        channel: PubSub,
        callback: SubscribeCallable,
        flush_remain_messages=True,
    ) -> None:
        while True:
            message = await channel.get_message(
                ignore_subscribe_messages=True,
                timeout=self._subscribes_tick,
            )
            if message is not None:
                if iscoroutinefunction(callback):
                    await callback(message)  # type: ignore[misc]
                elif isfunction(callback):
                    callback(message)
                else:
                    raise NotImplementedError

            if key in self._subscribes_exit:
                self._subscribes_exit.remove(key)
                break

        while flush_remain_messages:
            message = await channel.get_message(ignore_subscribe_messages=True)
            if message is not None:
                if iscoroutinefunction(callback):
                    await callback(message)  # type: ignore[misc]
                elif isfunction(callback):
                    callback(message)
                else:
                    raise NotImplementedError
            else:
                break

    def get_subscribe_channels(self) -> List[str]:
        return list(self._subscribes.keys())

    def get_subscribe_task(self, channel: str) -> Task:
        return self._subscribes[channel]

    def cancel_subscribe_task(self, channel: str) -> bool:
        return self._subscribes[channel].cancel()

    def exit_flag_subscribe(self, channel: str) -> None:
        self._subscribes_exit.add(channel)

    def exit_flag_subscribes(self) -> None:
        for channel in self._subscribes.keys():
            self._subscribes_exit.add(channel)

    async def wait_subscribe(self, channel: str) -> None:
        await self._subscribes[channel]

    async def subscribe(self, channel: str, callback: SubscribeCallable) -> None:
        pub_sub = self.redis.pubsub()
        await pub_sub.subscribe(channel)
        self._subscribes[channel] = create_task(
            self._subscribe_task(channel, pub_sub, callback)
        )

    async def publish(self, channel: str, value: bytes) -> None:
        await self.redis.publish(channel, value)

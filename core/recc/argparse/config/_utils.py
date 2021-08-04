# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from typing import Optional, Any, List, Iterable, Type, TypeVar, get_type_hints
from recc.argparse.config.global_config import GlobalConfig, get_global_config_members
from recc.argparse.argument import Argument

_T = TypeVar("_T")


def get_namespace(
    *cmdline: Any,
    usage: str,
    description: str,
    arguments: Iterable[Argument],
    namespace: Optional[Namespace] = None,
) -> Namespace:
    parser = ArgumentParser(
        usage=usage,
        description=description,
        add_help=False,
    )

    for arg in arguments:
        parser.add_argument(*arg.keys, **arg.kwargs)

    if namespace:
        result = namespace
    else:
        result = Namespace()

    args = [str(c) for c in cmdline if c is not None]
    _, argv = parser.parse_known_args(args, result)
    result.help_message = parser.format_help()
    result.unrecognized_arguments = argv
    return result


def get_config_members(cls: Type[_T], ignore_global_members=False) -> List[str]:
    assert issubclass(cls, GlobalConfig)
    members = [key for key, val in get_type_hints(cls).items()]
    if not ignore_global_members:
        return members
    global_members = get_global_config_members()
    return list(filter(lambda m: m not in global_members, members))

# -*- coding: utf-8 -*-

from typing import Any, Callable


YamlEncoder = Callable[[Any], str]
YamlDecoder = Callable[[str], Any]


def recc_yaml_encoder(_: Any) -> str:
    raise NotImplementedError


def recc_yaml_decoder(_: str) -> Any:
    raise NotImplementedError


_global_yaml_encoder: YamlEncoder = recc_yaml_encoder
_global_yaml_decoder: YamlDecoder = recc_yaml_decoder


def install_pyyaml_driver() -> bool:
    """
    Install PyYaml driver.
    """

    try:
        import yaml

        global _global_yaml_encoder
        global _global_yaml_decoder

        def yaml_encoder(data: Any) -> str:
            return yaml.dump(data)

        def yaml_decoder(data: str) -> Any:
            return yaml.full_load(data)

        _global_yaml_encoder = yaml_encoder
        _global_yaml_decoder = yaml_decoder

        return True
    except ImportError:
        return False


def global_yaml_encoder(data: Any) -> str:
    return _global_yaml_encoder(data)


def global_yaml_decoder(data: str) -> Any:
    return _global_yaml_decoder(data)


install_pyyaml_driver()

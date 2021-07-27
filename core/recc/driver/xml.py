# -*- coding: utf-8 -*-

from typing import Any, Callable


XmlEncoder = Callable[[Any], str]
XmlDecoder = Callable[[str], Any]


def recc_xml_encoder(_: Any) -> str:
    raise NotImplementedError


def recc_xml_decoder(_: str) -> Any:
    raise NotImplementedError


_global_xml_encoder: XmlEncoder = recc_xml_encoder
_global_xml_decoder: XmlDecoder = recc_xml_decoder


def install_xmltodict_driver() -> bool:
    """
    Install xmltodict driver.
    """

    try:
        import xmltodict

        global _global_xml_encoder
        global _global_xml_decoder

        def xmltodict_encoder(data: Any) -> str:
            return xmltodict.unparse(data)

        def xmltodict_decoder(data: str) -> Any:
            return xmltodict.parse(data)

        _global_xml_encoder = xmltodict_encoder
        _global_xml_decoder = xmltodict_decoder

        return True
    except ImportError:
        return False


def global_xml_encoder(data: Any) -> str:
    return _global_xml_encoder(data)


def global_xml_decoder(data: str) -> Any:
    return _global_xml_decoder(data)


install_xmltodict_driver()

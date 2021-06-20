# -*- coding: utf-8 -*-

import pickle
from typing import Optional, Dict, Any, Callable
from recc.driver.json import global_json_byte_encoder, global_json_byte_decoder
from recc.mime.mime_codec import MimeCodec
from recc.mime.mime_type import (
    APPLICATION_OCTET_STREAM,
    APPLICATION_JSON,
    TEXT_PLAIN,
)

MimeEncoder = Callable[[Any], bytes]
MimeDecoder = Callable[[bytes], Any]


def create_pickle_codec() -> MimeCodec:
    return MimeCodec(
        APPLICATION_OCTET_STREAM,
        lambda x: pickle.dumps(x),
        lambda x: pickle.loads(x),
    )


def create_text_codec() -> MimeCodec:
    return MimeCodec(
        TEXT_PLAIN,
        lambda x: str(x).encode(encoding="utf-8"),
        lambda x: str(x, encoding="utf-8"),
    )


def create_json_codec() -> MimeCodec:
    return MimeCodec(
        APPLICATION_JSON,
        global_json_byte_encoder,
        global_json_byte_decoder,
    )


class MimeCodecRegister:
    def __init__(self, default: Optional[MimeCodec] = None):
        self._mimes: Dict[str, MimeCodec] = dict()
        self._default = default if default else create_pickle_codec()

    @property
    def mimes(self):
        return self._mimes.keys()

    def exist(self, mime: str) -> bool:
        return mime in self._mimes.keys()

    def exist_encoder(self, mime: str) -> bool:
        return self.exist(mime) and self._mimes[mime].exist_encoder()

    def exist_decoder(self, mime: str) -> bool:
        return self.exist(mime) and self._mimes[mime].exist_decoder()

    def set_encoder(self, mime: str, encoder: MimeEncoder) -> None:
        if self.exist(mime):
            self._mimes[mime].set_encoder(encoder)
        else:
            self.add(mime, encoder=encoder)

    def set_decoder(self, mime: str, decoder: MimeDecoder) -> None:
        if self.exist(mime):
            self._mimes[mime].set_decoder(decoder)
        else:
            self.add(mime, decoder=decoder)

    def set_default_encoder(self, encoder: MimeEncoder) -> None:
        self._default.set_encoder(encoder)

    def set_default_decoder(self, decoder: MimeDecoder) -> None:
        self._default.set_decoder(decoder)

    def remove_encoder(self, mime: str) -> None:
        if self.exist(mime):
            self._mimes[mime].remove_encoder()

    def remove_decoder(self, mime: str) -> None:
        if self.exist(mime):
            self._mimes[mime].remove_decoder()

    def add(
        self,
        mime: str,
        encoder: Optional[MimeEncoder] = None,
        decoder: Optional[MimeDecoder] = None,
    ) -> None:
        self._mimes[mime] = MimeCodec(mime, encoder=encoder, decoder=decoder)

    def add_mime_codec(self, codec: MimeCodec) -> None:
        self._mimes[str(codec.mime)] = codec

    def remove(self, mime: str) -> None:
        del self._mimes[mime]

    def encode(self, mime: str, data: Any) -> bytes:
        if mime in self._mimes:
            return self._mimes[mime].encode(data)
        return self._default.encode(data)

    def decode(self, mime: str, data: bytes) -> Any:
        if mime in self._mimes:
            return self._mimes[mime].decode(data)
        return self._default.decode(data)

    def encode_json(self, data: Any) -> bytes:
        return self.encode(APPLICATION_JSON, data)

    def decode_json(self, data: bytes) -> Any:
        return self.decode(APPLICATION_JSON, data)

    def encode_text(self, data: Any) -> bytes:
        return self.encode(TEXT_PLAIN, data)

    def decode_text(self, data: bytes) -> Any:
        return self.decode(TEXT_PLAIN, data)

    def encode_binary(self, data: Any) -> bytes:
        return self.encode(APPLICATION_OCTET_STREAM, data)

    def decode_binary(self, data: bytes) -> Any:
        return self.decode(APPLICATION_OCTET_STREAM, data)

    def encode_default(self, data: Any) -> bytes:
        return self._default.encode(data)

    def decode_default(self, data: bytes) -> Any:
        return self._default.decode(data)

    @classmethod
    def default(cls):
        result = cls()
        result.add_mime_codec(create_text_codec())
        result.add_mime_codec(create_json_codec())
        return result


_GLOBAL_MIME_CODEC_REGISTER = MimeCodecRegister.default()


def get_global_mime_register() -> MimeCodecRegister:
    return _GLOBAL_MIME_CODEC_REGISTER


def global_mime_encoder(mime: str, data: Any) -> bytes:
    return _GLOBAL_MIME_CODEC_REGISTER.encode(mime, data)


def global_mime_decoder(mime: str, data: bytes) -> Any:
    return _GLOBAL_MIME_CODEC_REGISTER.decode(mime, data)

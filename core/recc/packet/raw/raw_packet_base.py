# -*- coding: utf-8 -*-

from typing import Iterable, Union, Optional, Mapping, List
from functools import reduce
from io import BytesIO
from recc.packet.raw.raw_field_spec import RawFieldSpec
from recc.inspect.member import get_public_attributes

DEFAULT_VERSION = 0


class RawPacketBase:

    _specs: Mapping[int, List[RawFieldSpec]]

    def __init__(
        self,
        specs: Union[Mapping[int, Iterable[RawFieldSpec]], Iterable[RawFieldSpec]],
        *,
        proofread_floor=False,
        proofread_ceil=False,
    ):
        if isinstance(specs, Mapping):
            self._specs = {k: list(v) for k, v in specs.items()}
        else:
            self._specs = {DEFAULT_VERSION: list(specs)}
        self.proofread_floor = proofread_floor
        self.proofread_ceil = proofread_ceil

    def get_packet_size(self, version=DEFAULT_VERSION) -> int:
        if version not in self._specs:
            raise ValueError(f"Unsupported version number: {version}")
        return reduce(lambda x, y: x + y, [f.size for f in self._specs[version]])

    def get_spec(self, key: Union[str, int], version=DEFAULT_VERSION) -> RawFieldSpec:
        if version not in self._specs:
            raise ValueError(f"Unsupported version number: {version}")
        if isinstance(key, int):
            return self._specs[version][key]
        else:
            assert isinstance(key, str)
            for spec in self._specs[version]:
                if spec.name == key:
                    return spec
            raise KeyError(f"Not found spec: {key}")

    def proofread_by_spec(self, spec: RawFieldSpec, value: int) -> int:
        if self.proofread_ceil:
            value_max = spec.max
            if value > value_max:
                return value_max
        if self.proofread_floor:
            value_min = spec.min
            if value < value_min:
                return value_min
        return value

    def proofread_by_key(
        self,
        key: str,
        value: int,
        version=DEFAULT_VERSION,
    ) -> int:
        return self.proofread_by_spec(self.get_spec(key, version), value)

    def to_dict(self) -> dict:
        return dict(get_public_attributes(self))

    def from_dict(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clear(self) -> None:
        for key, _ in get_public_attributes(self):
            setattr(self, key, type(getattr(self, key))())

    def to_bytes(self, version=DEFAULT_VERSION) -> bytes:
        if version not in self._specs:
            raise ValueError(f"Unsupported version number: {version}")

        buffer = BytesIO()
        for field in self._specs[version]:
            if not hasattr(self, field.name):
                raise KeyError(f"Not has `{field.name}` attribute")

            value = getattr(self, field.name)
            if not isinstance(value, int):
                msg1 = f"`{field.name}` is a `{type(field.name).__name__}` type."
                msg2 = "Only `int` types are allowed."
                raise TypeError(f"{msg1} {msg2}")

            encoded_value = value.to_bytes(
                field.size, field.byteorder, signed=field.signed
            )
            buffer.write(encoded_value)
        return buffer.getvalue()

    def to_hex(
        self,
        version=DEFAULT_VERSION,
        separator: Optional[Union[str, bytes]] = None,
    ) -> str:
        if separator:
            return self.to_bytes(version).hex(separator)
        else:
            return self.to_bytes(version).hex()

    def from_bytes(
        self,
        data: bytes,
        version=DEFAULT_VERSION,
        validation=True,
    ) -> None:
        if version not in self._specs:
            raise ValueError(f"Unsupported version number: {version}")

        buffer = BytesIO(data)
        for field in self._specs[version]:
            assert field.size >= 1
            encoded_value = buffer.read(field.size)

            if not encoded_value:
                raise EOFError("No more data.")

            value = int.from_bytes(encoded_value, field.byteorder, signed=field.signed)
            value = self.proofread_by_spec(field, value)

            if validation and field.range:
                if value not in field.range:
                    raise IndexError(f"`{field.name}` field is out of range")

            setattr(self, field.name, value)

    def from_hex(
        self,
        data: str,
        version=DEFAULT_VERSION,
        validation=True,
    ) -> None:
        self.from_bytes(bytes.fromhex(data), version, validation)

    def random(self, version=DEFAULT_VERSION) -> None:
        if version not in self._specs:
            raise ValueError(f"Unsupported version number: {version}")

        for field in self._specs[version]:
            if not hasattr(self, field.name):
                raise KeyError(f"Not has `{field.name}` attribute")
            setattr(self, field.name, field.random())

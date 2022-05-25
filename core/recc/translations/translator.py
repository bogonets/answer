# -*- coding: utf-8 -*-

import os
from json import loads as json_loads  # [WARNING] Don't use any other `json` driver.
from typing import Any, Dict, Final, Optional

from yaml import full_load as yaml_loads  # [WARNING] Don't use any other `yaml` driver.

# [IMPORTANT] Do not import files. Can be used in plugin projects.

LangCode = str
TransKey = str
TransValue = str
TransMap = Dict[TransKey, TransValue]
LangTransMap = Dict[LangCode, TransMap]

DEFAULT_TRANS_KEY_DELIMITER: Final[str] = "."
DEFAULT_LANGUAGE_CODE: Final[str] = "en"
DEFAULT_FALLBACK_LANGUAGE_CODE: Final[str] = "en"

_JSON_EXTENSIONS = (".json",)
_YAML_EXTENSIONS = (".yaml", ".yml")


def _read_file(path: str, encoding="utf-8") -> str:
    with open(path, "r", encoding=encoding) as f:
        return f.read()


def _decode_file(path: str, encoding="utf-8") -> Any:
    ext = os.path.splitext(path)[1]
    lower_ext = ext.lower()
    if lower_ext in _JSON_EXTENSIONS:
        return json_loads(_read_file(path, encoding))
    elif lower_ext in _YAML_EXTENSIONS:
        return yaml_loads(_read_file(path, encoding))
    else:
        raise ValueError(f"Unsupported file extension: '{ext}'")


def parse_to_trans_map(
    trans: dict,
    delimiter=DEFAULT_TRANS_KEY_DELIMITER,
) -> TransMap:
    result: TransMap = dict()
    for key, val in trans.items():
        if not isinstance(key, str):
            raise TypeError(f"`key` must be of type `str`: {type(key).__name__}")
        if isinstance(val, dict):
            for sub_key, sub_val in parse_to_trans_map(val, delimiter).items():
                result[key + delimiter + sub_key] = sub_val
        elif isinstance(val, str):
            result[key] = val
        elif isinstance(val, (int, float)):
            result[key] = str(val)
        else:
            raise TypeError(f"Unsupported `val` type: {type(val).__name__}")
    return result


def parse_to_lang_trans_map(
    root: Any,
    delimiter=DEFAULT_TRANS_KEY_DELIMITER,
) -> LangTransMap:
    if not isinstance(root, dict):
        raise TypeError(f"Root data must be of type 'dict': {type(root).__name__}")
    result: LangTransMap = dict()
    for lang, trans in root.items():
        if not isinstance(lang, str):
            raise TypeError(f"`lang` must be of type `str`: {type(lang).__name__}")
        if not isinstance(trans, dict):
            raise TypeError(f"`trans` must be of type `dict`: {type(trans).__name__}")
        result[lang] = parse_to_trans_map(trans, delimiter)
    return result


class Translator:
    def __init__(
        self,
        lang_trans_map: LangTransMap,
        lang=DEFAULT_LANGUAGE_CODE,
        fallback_lang=DEFAULT_FALLBACK_LANGUAGE_CODE,
    ):
        self._lang_trans_map = lang_trans_map
        self._lang = lang
        self._fallback_lang = fallback_lang

    @property
    def langs(self):
        return self._lang_trans_map.keys()

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value: str) -> None:
        self._lang = value

    @classmethod
    def from_dict(
        cls,
        root: Any,
        lang=DEFAULT_LANGUAGE_CODE,
        *,
        fallback_lang=DEFAULT_FALLBACK_LANGUAGE_CODE,
        delimiter=DEFAULT_TRANS_KEY_DELIMITER,
    ):
        return cls(parse_to_lang_trans_map(root, delimiter), lang, fallback_lang)

    @classmethod
    def from_dir(
        cls,
        path: str,
        lang=DEFAULT_LANGUAGE_CODE,
        *,
        fallback_lang=DEFAULT_FALLBACK_LANGUAGE_CODE,
        delimiter=DEFAULT_TRANS_KEY_DELIMITER,
        encoding="utf-8",
    ):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Not found directory: '{path}'")
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Not a directory: '{path}'")

        root = dict()
        for filename in os.listdir(path):
            base = os.path.splitext(filename)[0]
            try:
                root[base] = _decode_file(os.path.join(path, filename), encoding)
            except BaseException as e:  # noqa
                continue

        return cls(parse_to_lang_trans_map(root, delimiter), lang, fallback_lang)

    @classmethod
    def from_file(
        cls,
        path: str,
        lang=DEFAULT_LANGUAGE_CODE,
        *,
        fallback_lang=DEFAULT_FALLBACK_LANGUAGE_CODE,
        delimiter=DEFAULT_TRANS_KEY_DELIMITER,
        encoding="utf-8",
    ):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Not found file: '{path}'")
        if not os.path.isfile(path):
            raise NotADirectoryError(f"Not a file: '{path}'")
        root = _decode_file(path, encoding)
        return cls(parse_to_lang_trans_map(root, delimiter), lang, fallback_lang)

    def get(self, key: TransKey, lang: Optional[LangCode] = None) -> TransValue:
        lang_code = lang if lang else self._lang
        try:
            return self._lang_trans_map[lang_code][key]
        except:  # noqa
            if lang_code == self._fallback_lang:
                raise
            else:
                return self._lang_trans_map[self._fallback_lang][key]

    def tl(self, lang: LangCode, key: TransKey, *args, **kwargs) -> TransValue:
        value = self._lang_trans_map[lang][key]
        if args or kwargs:
            return value.format(*args, **kwargs)
        else:
            return value

    def tm(self, key: TransKey, *args, **kwargs) -> Dict[LangCode, TransValue]:
        result = dict()
        for lang in self.langs:
            try:
                result[lang] = self.tl(lang, key, *args, **kwargs)
            except:  # noqa
                continue
        return result

    def t(self, key: TransKey, *args, **kwargs) -> TransValue:
        value = self.get(key)
        if args or kwargs:
            return value.format(*args, **kwargs)
        else:
            return value

    def __call__(self, key: TransKey, *args, **kwargs):
        return self.t(key, *args, **kwargs)


class TranslatorLangMapper(Translator):
    def __init__(
        self,
        lang_trans_map: LangTransMap,
        lang=DEFAULT_LANGUAGE_CODE,
        fallback_lang=DEFAULT_FALLBACK_LANGUAGE_CODE,
    ):
        super().__init__(lang_trans_map, lang, fallback_lang)

    def __call__(self, key: TransKey, *args, **kwargs):
        return self.tm(key, *args, **kwargs)

# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, Type, TypeVar

from type_serialize import Serializable, deserialize, serialize

from recc.serialization.utils import update_dict
from recc.template.dependency import Dependency
from recc.template.environment import Environment
from recc.template.locale import Locale
from recc.template.v2 import keys as v2k

EDGE_BEGIN = "begin"
EDGE_MIDDLE = "middle"
EDGE_END = "begin"

_T = TypeVar("_T")


def strip_optional(obj: Any, cls: Type[_T]) -> _T:
    if obj is None:
        return cls()
    else:
        return obj


class Information(Serializable):
    name: Optional[str] = None
    script_path: Optional[str] = None
    version: Optional[str] = None
    category: Optional[str] = None
    keywords: Optional[List[str]] = None
    homepage: Optional[str] = None
    bugs: Optional[str] = None
    license_name: Optional[str] = None
    license_text: Optional[str] = None
    author: Optional[str] = None
    dependencies: Optional[List[Dependency]] = None
    engines: Optional[List[str]] = None
    environment: Optional[Environment] = None
    titles: Optional[Locale] = None
    descriptions: Optional[Locale] = None
    documentation_mime: Optional[str] = None
    documentations: Optional[Locale] = None
    edge: Optional[str] = None
    meta: Any = None

    def get_name(self) -> str:
        return strip_optional(self.name, str)

    def get_script_path(self) -> str:
        return strip_optional(self.script_path, str)

    def get_version(self) -> str:
        return strip_optional(self.version, str)

    def get_category(self) -> str:
        return strip_optional(self.category, str)

    def get_keywords(self) -> List[str]:
        return strip_optional(self.keywords, list)

    def get_homepage(self) -> str:
        return strip_optional(self.homepage, str)

    def get_bugs(self) -> str:
        return strip_optional(self.bugs, str)

    def get_license_name(self) -> str:
        return strip_optional(self.license_name, str)

    def get_license_text(self) -> str:
        return strip_optional(self.license_text, str)

    def get_author(self) -> str:
        return strip_optional(self.author, str)

    def get_dependencies(self) -> List[Dependency]:
        return strip_optional(self.dependencies, list)

    def get_engines(self) -> List[str]:
        return strip_optional(self.engines, list)

    def get_environment(self) -> Environment:
        return strip_optional(self.environment, Environment)

    def get_titles(self) -> Locale:
        return strip_optional(self.titles, Locale)

    def get_descriptions(self) -> Locale:
        return strip_optional(self.descriptions, Locale)

    def get_documentation_mime(self) -> str:
        return strip_optional(self.documentation_mime, str)

    def get_documentations(self) -> Locale:
        return strip_optional(self.documentations, Locale)

    def get_edge(self) -> str:
        return strip_optional(self.edge, str)

    def clear(self) -> None:
        self.name = None
        self.script_path = None
        self.version = None
        self.category = None
        self.keywords = None
        self.homepage = None
        self.bugs = None
        self.license_name = None
        self.license_text = None
        self.author = None
        self.dependencies = None
        self.engines = None
        self.environment = None
        self.titles = None
        self.descriptions = None
        self.documentation_mime = None
        self.documentations = None
        self.edge = None
        self.meta = None

    def __serialize__(self) -> Any:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_category, self.category)
        update_dict(result, v2k.k_name, self.name)
        update_dict(result, v2k.k_script_path, self.script_path)
        update_dict(result, v2k.k_version, self.version)
        update_dict(result, v2k.k_category, self.category)
        update_dict(result, v2k.k_keywords, self.keywords)
        update_dict(result, v2k.k_homepage, self.homepage)
        update_dict(result, v2k.k_bugs, self.bugs)
        update_dict(result, v2k.k_license_name, self.license_name)
        update_dict(result, v2k.k_license_text, self.license_text)
        update_dict(result, v2k.k_author, self.author)

        if self.dependencies is not None:
            result[v2k.k_dependencies] = serialize(self.dependencies)
        update_dict(result, v2k.k_engines, self.engines)
        if self.environment is not None:
            result[v2k.k_environment] = serialize(self.environment)

        if self.titles is not None:
            result[v2k.k_titles] = serialize(self.titles)
        if self.descriptions is not None:
            result[v2k.k_descriptions] = serialize(self.descriptions)
        update_dict(result, v2k.k_documentation_mime, self.documentation_mime)
        if self.documentations is not None:
            result[v2k.k_documentations] = serialize(self.documentations)
        update_dict(result, v2k.k_edge, self.edge)
        update_dict(result, v2k.k_meta, self.meta)

        return result

    def __deserialize__(self, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError
        self.name = data.get(v2k.k_name)
        self.script_path = data.get(v2k.k_script_path)
        self.version = data.get(v2k.k_version)
        self.category = data.get(v2k.k_category)
        self.keywords = data.get(v2k.k_keywords)
        self.homepage = data.get(v2k.k_homepage)
        self.bugs = data.get(v2k.k_bugs)
        self.license_name = data.get(v2k.k_license_name)
        self.license_text = data.get(v2k.k_license_text)
        self.author = data.get(v2k.k_author)

        dependency_val = data.get(v2k.k_dependencies)
        self.dependencies = deserialize(dependency_val, Optional[List[Dependency]])

        self.engines = data.get(v2k.k_engines)

        self.environment = Environment()
        self.environment.__deserialize__(data.get(v2k.k_environment))

        titles_val = data.get(v2k.k_titles)
        descriptions_val = data.get(v2k.k_descriptions)
        documentations_val = data.get(v2k.k_documentations)
        self.titles = deserialize(titles_val, Optional[Locale])
        self.descriptions = deserialize(descriptions_val, Optional[Locale])
        self.documentation_mime = data.get(v2k.k_documentation_mime)
        self.documentations = deserialize(documentations_val, Optional[Locale])
        self.edge = data.get(v2k.k_edge)
        self.meta = data.get(v2k.k_meta)

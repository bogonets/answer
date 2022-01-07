# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List
from recc.typing.optional import strip_optional
from recc.serialization.utils import update_dict, normalize_strings
from recc.serialization.interface import Serializable
from recc.serialization.deserialize import deserialize
from recc.serialization.serialize import serialize
from recc.template.dependency import Dependency
from recc.template.environment import Environment
from recc.template.locale import Locale
from recc.template.v1 import keys as v1k
from recc.template.v2 import keys as v2k

EDGE_BEGIN = "begin"
EDGE_MIDDLE = "middle"
EDGE_END = "begin"


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

    def serialize(self, version: int) -> Any:
        if version == 1:
            return self.serialize_v1()
        else:
            return self.serialize_v2()

    def deserialize(self, version: int, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if version == 1:
            self.deserialize_v1(data)
        else:
            self.deserialize_v2(data)

    def deserialize_v1(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.name = data.get(v1k.k_name)
        self.script_path = data.get(v1k.k_script_path)
        self.version = data.get(v1k.k_version)
        self.category = data.get(v1k.k_category)
        self.keywords = normalize_strings(data.get(v1k.k_keywords))
        self.homepage = data.get(v1k.k_homepage)
        self.bugs = data.get(v1k.k_bugs)
        self.license_name = None
        self.license_text = data.get(v1k.k_license)
        self.author = data.get(v1k.k_author)

        dependency_val = data.get(v1k.k_dependencies)
        dependency_hint = Optional[List[Dependency]]
        self.dependencies = deserialize(1, dependency_val, list, dependency_hint)

        self.engines = normalize_strings(data.get(v1k.k_engines))

        self.environment = Environment()
        self.environment.deserialize(1, data.get(v1k.k_environment))

        locale_hint = Optional[Locale]
        titles_val = data.get(v1k.k_titles)
        descriptions_val = data.get(v1k.k_descriptions)
        documentations_val = data.get(v1k.k_documentations)
        self.titles = deserialize(1, titles_val, Locale, locale_hint)
        self.descriptions = deserialize(1, descriptions_val, Locale, locale_hint)
        self.documentation_mime = data.get(v1k.k_documentation_mime)
        self.documentations = deserialize(1, documentations_val, Locale, locale_hint)

        self.meta = data.get(v1k.k_meta)

    def serialize_v1(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v1k.k_category, self.category)
        update_dict(result, v1k.k_name, self.name)
        update_dict(result, v1k.k_script_path, self.script_path)
        update_dict(result, v1k.k_version, self.version)
        update_dict(result, v1k.k_category, self.category)
        update_dict(result, v1k.k_keywords, self.keywords)
        update_dict(result, v1k.k_homepage, self.homepage)
        update_dict(result, v1k.k_bugs, self.bugs)
        update_dict(result, v1k.k_license, self.license_text)
        update_dict(result, v1k.k_author, self.author)

        if self.dependencies is not None:
            result[v1k.k_dependencies] = serialize(1, self.dependencies)
        update_dict(result, v1k.k_engines, self.engines)
        if self.environment is not None:
            result[v1k.k_environment] = serialize(1, self.environment)

        if self.titles is not None:
            result[v1k.k_titles] = serialize(1, self.titles)
        if self.descriptions is not None:
            result[v1k.k_descriptions] = serialize(1, self.descriptions)
        update_dict(result, v1k.k_documentation_mime, self.documentation_mime)
        if self.documentations is not None:
            result[v1k.k_documentations] = serialize(1, self.documentations)

        update_dict(result, v1k.k_meta, self.meta)
        return result

    def deserialize_v2(self, data: Any) -> None:
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
        dependency_hint = Optional[List[Dependency]]
        self.dependencies = deserialize(2, dependency_val, list, dependency_hint)

        self.engines = data.get(v2k.k_engines)

        self.environment = Environment()
        self.environment.deserialize(2, data.get(v2k.k_environment))

        locale_hint = Optional[Locale]
        titles_val = data.get(v2k.k_titles)
        descriptions_val = data.get(v2k.k_descriptions)
        documentations_val = data.get(v2k.k_documentations)
        self.titles = deserialize(2, titles_val, Locale, locale_hint)
        self.descriptions = deserialize(2, descriptions_val, Locale, locale_hint)
        self.documentation_mime = data.get(v2k.k_documentation_mime)
        self.documentations = deserialize(2, documentations_val, Locale, locale_hint)
        self.edge = data.get(v2k.k_edge)
        self.meta = data.get(v2k.k_meta)

    def serialize_v2(self) -> Dict[str, Any]:
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
            result[v2k.k_dependencies] = serialize(2, self.dependencies)
        update_dict(result, v2k.k_engines, self.engines)
        if self.environment is not None:
            result[v2k.k_environment] = serialize(2, self.environment)

        if self.titles is not None:
            result[v2k.k_titles] = serialize(2, self.titles)
        if self.descriptions is not None:
            result[v2k.k_descriptions] = serialize(2, self.descriptions)
        update_dict(result, v2k.k_documentation_mime, self.documentation_mime)
        if self.documentations is not None:
            result[v2k.k_documentations] = serialize(2, self.documentations)
        update_dict(result, v2k.k_edge, self.edge)
        update_dict(result, v2k.k_meta, self.meta)

        return result

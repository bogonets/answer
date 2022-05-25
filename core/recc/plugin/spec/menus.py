# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from recc.packet.plugin import PluginMenuA, PluginMenusA
from recc.variables.plugin import (
    SPEC_MENU_ITEM_PROP_ICON,
    SPEC_MENU_ITEM_PROP_LANG,
    SPEC_MENU_ITEM_PROP_NAME,
    SPEC_MENU_ITEM_PROP_PATH,
    SPEC_MENUS,
    SPEC_MENUS_CATEGORY_ADMIN,
    SPEC_MENUS_CATEGORY_GROUP,
    SPEC_MENUS_CATEGORY_PROJECT,
    SPEC_MENUS_CATEGORY_USER,
)


def parse_spec_menu_category_item(element: Any) -> PluginMenuA:
    if not isinstance(element, dict):
        type_name = type(element).__name__
        raise TypeError(f"Menu `elements` must be of type 'dict': {type_name}")

    icon = element.get(SPEC_MENU_ITEM_PROP_ICON, str())
    name = element.get(SPEC_MENU_ITEM_PROP_NAME, str())
    path = element.get(SPEC_MENU_ITEM_PROP_PATH, str())
    lang = element.get(SPEC_MENU_ITEM_PROP_LANG, dict())

    if not isinstance(icon, str):
        prop = SPEC_MENU_ITEM_PROP_ICON
        type_name = type(icon).__name__
        raise TypeError(f"Menu `{prop}` must be of type 'str': {type_name}")
    if not isinstance(name, str):
        prop = SPEC_MENU_ITEM_PROP_NAME
        type_name = type(name).__name__
        raise TypeError(f"Menu `{prop}` must be of type 'str': {type_name}")
    if not isinstance(path, str):
        prop = SPEC_MENU_ITEM_PROP_PATH
        type_name = type(path).__name__
        raise TypeError(f"Menu `{prop}` must be of type 'str': {type_name}")
    if not isinstance(lang, dict):
        prop = SPEC_MENU_ITEM_PROP_LANG
        type_name = type(lang).__name__
        raise TypeError(f"Menu `{prop}` must be of type 'dict': {type_name}")

    return PluginMenuA(icon, name, path, lang)


def parse_spec_menu_category(category: Any) -> List[PluginMenuA]:
    if not isinstance(category, (tuple, list)):
        prefix = "Menu `category` must be of type 'tuple' or 'list'"
        message = f"{prefix}: {type(category).__name__}"
        raise TypeError(message)
    return [parse_spec_menu_category_item(i) for i in category]


def parse_spec_menus(spec: Dict[str, Any]) -> PluginMenusA:
    if SPEC_MENUS not in spec:
        return PluginMenusA(
            admin=list(),
            group=list(),
            project=list(),
            user=list(),
        )

    menus = spec[SPEC_MENUS]
    if not isinstance(menus, dict):
        raise TypeError(f"Unsupported `{SPEC_MENUS}` type: {type(menus).__name__}")

    admin = parse_spec_menu_category(menus.get(SPEC_MENUS_CATEGORY_ADMIN, list()))
    group = parse_spec_menu_category(menus.get(SPEC_MENUS_CATEGORY_GROUP, list()))
    project = parse_spec_menu_category(menus.get(SPEC_MENUS_CATEGORY_PROJECT, list()))
    user = parse_spec_menu_category(menus.get(SPEC_MENUS_CATEGORY_USER, list()))

    return PluginMenusA(
        admin=admin,
        group=group,
        project=project,
        user=user,
    )

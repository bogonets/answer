# -*- coding: utf-8 -*-

import os

from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import STATIC_WEB_FILES_DIRECTORY_NAME, STATIC_WEB_INDEX_HTML


class PluginWww(PluginBase):
    @property
    def www_dir(self) -> str:
        return os.path.join(self.module_directory, STATIC_WEB_FILES_DIRECTORY_NAME)

    @property
    def index_html_path(self) -> str:
        return os.path.join(self.www_dir, STATIC_WEB_INDEX_HTML)

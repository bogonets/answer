# -*- coding: utf-8 -*-

from typing import Optional
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment


class RuntimeInformation:

    template_filename: Optional[str] = None
    template_path: Optional[str] = None
    script_filename: Optional[str] = None
    script_path: Optional[str] = None
    script_content: Optional[str] = None
    optimize: Optional[int] = None
    template_directory: Optional[str] = None
    venv: Optional[AsyncVirtualEnvironment] = None

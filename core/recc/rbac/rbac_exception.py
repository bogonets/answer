# -*- coding: utf-8 -*-


class RbacKeyError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RbacMismatchContextError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RbacPermissionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

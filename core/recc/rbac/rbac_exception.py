# -*- coding: utf-8 -*-


class RbacError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RbacKeyError(RbacError):
    def __init__(self, *args):
        super().__init__(*args)


class RbacMismatchContextError(RbacError):
    def __init__(self, *args):
        super().__init__(*args)


class RbacPermissionError(RbacError):
    def __init__(self, *args):
        super().__init__(*args)

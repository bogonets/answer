# -*- coding: utf-8 -*-


def singleton(base):
    class _Class(base):

        __instance = None

        def __new__(cls, *args, **kwargs):
            if _Class.__instance is None:
                _Class.__instance = super(_Class, cls).__new__(cls, *args, **kwargs)
                _Class.__instance.__sealed = False
            return _Class.__instance

        def __init__(self, *args, **kwargs):
            if self.__sealed:
                return
            super(_Class, self).__init__(*args, **kwargs)
            self.__sealed = True

    _Class.__name__ = base.__name__

    return _Class

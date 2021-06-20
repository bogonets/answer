# -*- coding: utf-8 -*-


class CreateTableError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class SelectError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class UpdateError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class InsertError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class DeleteError(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)

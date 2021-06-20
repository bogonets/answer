# -*- coding: utf-8 -*-


class _Structure:
    """
    Common structure.
    """

    def __eq__(self, other) -> bool:
        return vars(self) == vars(other)

    def __ne__(self, other) -> bool:
        return vars(self) != vars(other)

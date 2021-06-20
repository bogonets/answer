# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class SequencerInterface(metaclass=ABCMeta):
    """
    Sequencer interface.
    """

    @abstractmethod
    def next(self) -> int:
        raise NotImplementedError

# -*- coding: utf-8 -*-

from recc.sequence.sequencer_interface import SequencerInterface


class DefaultSequencer(SequencerInterface):
    def __init__(self, begin=0, step=1):
        self._cursor = begin
        self._begin = begin
        self._step = step

    @property
    def cursor(self) -> int:
        return self._cursor

    @property
    def begin(self) -> int:
        return self._begin

    @property
    def step(self) -> int:
        return self._step

    def next(self) -> int:
        result = self._cursor
        self._cursor += self._step
        return result

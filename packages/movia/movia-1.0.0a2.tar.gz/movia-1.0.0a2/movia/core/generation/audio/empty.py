#!/usr/bin/env python3

"""
** Dedicated to tests, it is an empty audio stream containing no samples. **
----------------------------------------------------------------------------
"""


import numbers
import typing

import numpy as np

from movia.core.classes.container import ContainerInput
from movia.core.classes.stream import Stream
from movia.core.classes.stream_audio import StreamAudio
from movia.core.exceptions import OutOfTimeRange



class GeneratorAudioEmpty(ContainerInput):
    """
    ** Contains an empty audio stream. **

    Examples
    --------
    >>> from movia.core.exceptions import OutOfTimeRange
    >>> from movia.core.generation.audio.empty import GeneratorAudioEmpty
    >>> (stream,) = GeneratorAudioEmpty().out_streams
    >>> try:
    ...     _ = stream.snapshot(0)
    ...     print("unreachable")
    ... except OutOfTimeRange as err:
    ...     print(err)
    ...
    this stream does not contain any samples
    >>>
    """

    def __init__(self):
        out_streams = [_StreamAudioEmpty(self)]
        super().__init__(out_streams)

    @classmethod
    def default(cls):
        return cls()

    def getstate(self) -> dict:
        return {}

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state == {}, state
        GeneratorAudioEmpty.__init__(self)


class _StreamAudioEmpty(StreamAudio):
    """
    ** An audio stream containing no sample. **
    """

    is_time_continuous = True

    def __init__(self, node: GeneratorAudioEmpty):
        assert isinstance(node, GeneratorAudioEmpty), node.__class__.__name__
        super().__init__(node)

    def _snapshot(self, timestamp: np.ndarray[numbers.Real]) -> np.ndarray[numbers.Real]:
        raise OutOfTimeRange("this stream does not contain any samples")

    @property
    def channels(self) -> int:
        raise KeyError("it makes no sense to give a number of channels to an absence of sample")

    @property
    def duration(self) -> numbers.Real:
        return 0

#!/usr/bin/env python3

"""
** Allows you to temporarily limit a sequence. **
-------------------------------------------------
"""



import fractions
import math
import numbers
import typing

import av
import numpy as np

from movia.core.classes.filter import Filter
from movia.core.classes.stream import Stream
from movia.core.classes.stream_audio import StreamAudio, StreamAudioWrapper
from movia.core.classes.stream_video import StreamVideo, StreamVideoWrapper
from movia.core.exceptions import OutOfTimeRange
from movia.core.generation.audio.noise import GeneratorAudioNoise
from movia.core.generation.video.noise import GeneratorVideoNoise



class FilterTruncate(Filter):
    """
    ** Shortens the duration of a stream. **

    Attributes
    ----------
    duration_max : fractions.Fraction
        The maximum duration beyond which the flows do not return anything (readonly).
    """

    def __init__(self, in_streams: typing.Iterable[Stream], duration_max: numbers.Real):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Forwarded to ``movia.core.classes.filter.Filter``.
        duration_max : numbers.Real
            The streams will be cut strictly after this duration in seconds.
        """
        assert hasattr(in_streams, "__iter__"), in_streams.__class__.__name__
        in_streams = tuple(in_streams)
        assert all(isinstance(stream, Stream) for stream in in_streams), \
            [stream.__class__.__name__ for stream in in_streams]
        assert isinstance(duration_max, numbers.Real), duration_max.__class__.__name__
        assert duration_max >= 0, duration_max

        try:
            self._duration_max = fractions.Fraction(duration_max)
        except OverflowError:
            self._duration_max = math.inf
        super().__init__(in_streams, in_streams) # solve recusrive initialisation
        out_streams = [
            self._select_stream(in_stream, index) for index, in_stream in enumerate(in_streams)
        ]
        super().__init__(in_streams, out_streams)

    def _select_stream(self, in_stream, index):
        if isinstance(in_stream, StreamVideo):
            return _StreamVideoTruncate(self, index)
        if isinstance(in_stream, StreamAudio):
            return _StreamAudioTruncate(self, index)
        raise NotImplementedError(
            f"the FilterTruncate does not support {in_stream.__class__.__name__} streams"
        )

    @classmethod
    def default(cls):
        audio_stream = GeneratorAudioNoise.default().out_streams[0]
        video_stream = GeneratorVideoNoise.default().out_streams[0]
        return cls([audio_stream, video_stream], 1)

    @property
    def duration_max(self) -> fractions.Fraction:
        """
        ** The maximum duration beyond which the flows do not return anything. **
        """
        return self._duration_max

    def getstate(self) -> dict:
        return {"duration_max": str(self.duration_max)}

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"duration_max"}, set(state)-{"duration_max"}
        if state["duration_max"] == "inf":
            duration_max = math.inf
        else:
            duration_max = fractions.Fraction(state["duration_max"])
        FilterTruncate.__init__(self, in_streams, duration_max)


class _StreamAudioTruncate(StreamAudioWrapper):
    """
    ** Truncates the end of a video stream after a certain time. **
    """

    def _snapshot(self, timestamp: np.ndarray[numbers.Real]) -> np.ndarray[numbers.Real]:
        if np.max(timestamp) >= self.beginning + self.duration:
            raise OutOfTimeRange(
                f"the stream has been truncated over {self.beginning+self.duration} seconds, "
                f"evaluation at {np.max(timestamp)} seconds"
            )
        return self.stream._snapshot(timestamp)

    @property
    def duration(self):
        return min(self.node.duration_max, self.stream.duration)


class _StreamVideoTruncate(StreamVideoWrapper):
    """
    ** Truncates the end of a video stream after a certain time. **
    """

    def _snapshot(self, timestamp: float) -> av.video.frame.VideoFrame:
        if timestamp >= self.beginning + self.duration:
            raise OutOfTimeRange(
                f"the stream has been truncated over {self.beginning+self.duration} seconds, "
                f"evaluation at {timestamp} seconds"
            )
        return self.stream._snapshot(timestamp)

    @property
    def duration(self):
        return min(self.node.duration_max, self.stream.duration)

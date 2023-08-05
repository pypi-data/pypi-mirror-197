#!/usr/bin/env python3

"""
** Defines the structure of an abstract audio stream. **
--------------------------------------------------------
"""

import abc
import numbers
import typing

import numpy as np

from movia.core.classes.filter import Filter
from movia.core.classes.stream import Stream, StreamWrapper
from movia.core.exceptions import OutOfTimeRange



class StreamAudio(Stream):
    """
    ** Representation of any audio stream. **

    Attributes
    ----------
    channels : int
        The number of tracks (readonly).
    """

    @property
    @abc.abstractmethod
    def channels(self) -> int:
        """
        ** The number of channels in this audio stream. **
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _snapshot(self, timestamp: np.ndarray[numbers.Real]) -> np.ndarray[numbers.Real]:
        raise NotImplementedError

    def snapshot(
        self, timestamp: typing.Union[numbers.Real, np.ndarray[numbers.Real]]
    ) -> np.ndarray[numbers.Real]:
        """
        ** Extract the closest values to the requested date. **

        Parameters
        ----------
        timestamps : numbers.Real or np.ndarray[numbers.Real]
            The time expressed in seconds since the beginning of the audio.
            Vector in 0 or 1 dimension.

        Returns
        -------
        sample : np.ndarray[numbers.Real]
            Audio samples corresponding to the times provided.
            This vector is of shape (nbr_channels, *timestamp_shape).
            The values are between -1 and 1.

        Raises
        ------
        movia.core.exception.OutOfTimeRange
            If we try to read a sample at a negative time or after the end of the stream.
        """
        # cast
        timestamp = np.asarray(timestamp)
        if timestamp.ndim != 1:
            return self.snapshot(timestamp.ravel()).reshape((-1, *timestamp.shape))

        # verification
        if timestamp.dtype == np.dtype("O"):
            assert all(isinstance(o, numbers.Real) for o in timestamp), timestamp
            timestamp = timestamp.astype(np.float64)
        else:
            assert issubclass(timestamp.dtype.type, numbers.Real), timestamp.dtype.type
        t_min = np.min(timestamp)
        if t_min < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {t_min} (need >= 0)")

        # evaluation
        sample = self._snapshot(timestamp)

        # verification
        assert sample.shape[1:] == timestamp.shape, (sample.shape, timestamp.shape)
        if sample.dtype == np.dtype("O"):
            assert all(isinstance(o, numbers.Real) for o in sample), sample
        else:
            assert issubclass(sample.dtype.type, numbers.Real), sample.dtype.type
        sample_no_nan = np.nan_to_num(sample)
        assert -1 <= np.min(sample_no_nan) and np.max(sample_no_nan) <= 1, \
            (np.nanmin(sample), np.nanmax(sample))

        return sample

    @property
    def type(self) -> str:
        return "audio"

class StreamAudioWrapper(StreamWrapper, StreamAudio):
    """
    ** Allows to dynamically transfer the methods of an instanced audio stream. **

    This can be very useful for implementing filters.
    """

    def __init__(self, node: Filter, index: numbers.Integral):
        """
        Parameters
        ----------
        filter : movia.core.classes.filter.Filter
            The parent node, transmitted to ``movia.core.classes.stream.Stream``.
        index : number.Integral
            The index of the audio stream among all the input streams of the ``node``.
            0 for the first, 1 for the second ...
        """
        assert isinstance(node, Filter), node.__class__.__name__
        assert len(node.in_streams) > index, f"only {len(node.in_streams)} streams, no {index}"
        assert isinstance(node.in_streams[index], StreamAudio), "the stream must be audio type"
        super().__init__(node, index)

    def _snapshot(self, timestamp: np.ndarray[numbers.Real]) -> np.ndarray[numbers.Real]:
        return self.stream._snapshot(timestamp)

    @property
    def channels(self) -> int:
        return self.stream.channels

#!/usr/bin/env python3

"""
** Defines the structure of an abstract video stream. **
--------------------------------------------------------
"""

import abc
import numbers

import av

from movia.core.classes.filter import Filter
from movia.core.classes.stream import Stream, StreamWrapper
from movia.core.exceptions import OutOfTimeRange



class StreamVideo(Stream):
    """
    ** Representation of any video stream. **

    Attributes
    ----------
    height : int
        Height of the image in pixels (readonly).
    is_space_continuous : boolean
        True if the data is continuous in the spacial domain, False if it is discrete (readonly).
    width : int
        Width of the image in pixels (readonly).
    """

    def _snapshot(self, timestamp: float) -> av.video.frame.VideoFrame:
        raise NotImplementedError

    @property
    def height(self) -> int:
        """
        ** Height of all images in the stream. **
        """
        if self.is_space_continuous and hasattr(self.node, "shape"):
            return self.node.shape[0]
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def is_space_continuous(self) -> bool:
        """
        ** True if the data is continuous in the spacial domain, False if it is discrete. **
        """
        raise NotImplementedError

    def snapshot(self, timestamp: numbers.Real) -> av.video.frame.VideoFrame:
        """
        ** Extract the closest frame to the requested date. **

        Parameters
        ----------
        timestamp : numbers.Real
            The time expressed in seconds since the beginning of the video.

        Returns
        -------
        frame : av.frame.Frame
            Video frame with metadata.

        Raises
        ------
        movia.core.exception.OutOfTimeRange
            If we try to read a frame at a negative time or after the end of the stream.
        """
        assert isinstance(timestamp, numbers.Real), timestamp.__class__.__name__
        if timestamp < 0:
            raise OutOfTimeRange(f"the timestamp must be positive or zero, it is {timestamp}")
        frame = self._snapshot(float(timestamp))
        assert isinstance(frame, av.video.frame.VideoFrame), frame.__class__.__name__
        return frame

    @property
    def type(self) -> str:
        return "video"

    @property
    def width(self) -> int:
        """
        ** Width of all images in the stream. **
        """
        if self.is_space_continuous and hasattr(self.node, "shape"):
            return self.node.shape[1]
        raise NotImplementedError


class StreamVideoWrapper(StreamWrapper, StreamVideo):
    """
    ** Allows to dynamically transfer the methods of an instanced video stream. **

    This can be very useful for implementing filters.

    Attribute
    ---------
    stream : movia.core.classes.stream_video.StreamVideo
        The video stream containing the properties to be transferred (readonly).
        This stream is one of the input streams of the parent node.
    """

    def __init__(self, node: Filter, index: numbers.Integral):
        """
        Parameters
        ----------
        filter : movia.core.classes.filter.Filter
            The parent node, transmitted to ``movia.core.classes.stream.Stream``.
        index : number.Integral
            The index of the video stream among all the input streams of the ``node``.
            0 for the first, 1 for the second ...
        """
        assert isinstance(node, Filter), node.__class__.__name__
        assert len(node.in_streams) > index, f"only {len(node.in_streams)} streams, no {index}"
        assert isinstance(node.in_streams[index], StreamVideo), "the stream must be video type"
        super().__init__(node, index)

    def _snapshot(self, timestamp: float) -> av.video.frame.VideoFrame:
        return self.stream._snapshot(timestamp)

    @property
    def height(self) -> int:
        return self.stream.height

    @property
    def is_space_continuous(self) -> bool:
        return self.stream.is_space_continuous

    @property
    def width(self) -> int:
        return self.stream.width

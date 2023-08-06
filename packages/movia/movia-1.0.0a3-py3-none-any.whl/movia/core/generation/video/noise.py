#!/usr/bin/env python3

"""
** Generate a video noise signal. **
------------------------------------
"""

import fractions
import numbers
import random
import struct
import typing

import av
import numpy as np

from movia.core.classes.container import ContainerInput
from movia.core.classes.stream import Stream
from movia.core.classes.stream_video import StreamVideo



class GeneratorVideoNoise(ContainerInput):
    """
    ** Generate a pure noise video signal. **

    Attributes
    ----------
    seed : float
        The value of the seed between 0 and 1 (readonly).
    shape : tuple[int, int]
        The vertical and horizontal (i, j) resolution of the image (readonly).

    Examples
    --------
    >>> from movia.core.generation.video.noise import GeneratorVideoNoise
    >>> stream = GeneratorVideoNoise(0, shape=(13, 9)).out_streams[0]
    >>> stream.snapshot(0).to_ndarray(format="bgr24")[..., 0]
    array([[ 95, 217,  15, 215, 248,  69, 205,  61,  29],
           [ 19,  59,  81, 120, 208,  64,  89, 127, 128],
           [ 76, 154,  95, 186, 220,   1, 237, 143,  96],
           [ 55,  77, 208, 190, 120, 240, 100, 126, 149],
           [115,   8, 207, 179, 166, 216, 247, 127,  58],
           [220, 168,  51,  56,  20, 185, 214, 207, 108],
           [ 58, 245, 104,   1, 209, 235, 169, 171, 142],
           [ 54,  49,  65, 137,  26,  51,  98, 254,  38],
           [ 63, 206,  24, 113, 243, 175,  57, 127, 188],
           [215,  62, 105, 188,  99,  10, 175,  21, 148],
           [179, 106, 241, 134,  27,   2,  24, 108,  95],
           [179, 134, 227, 172, 121, 156, 136, 152, 165],
           [107, 146,  45,   8, 163, 184,  36, 148, 158]], dtype=uint8)
    >>>
    """
    def __init__(self,
        seed: numbers.Real=None, shape: tuple[numbers.Integral, numbers.Integral]=(720, 720)
    ):
        """
        Parameters
        ----------
        seed : numbers.Real
            The random seed to have a repeatability.
            The value must be between 0 included and 1 excluded.
            If not provided, the seed is chosen randomly.
        shape : tuple[number.Integral, number.Integral], optional
            The pixel dimensions of the generated frames.
            The convention adopted is the numpy convention (height, width)
        """
        # check
        if seed is None:
            seed = random.random()
        assert isinstance(seed, numbers.Real), seed.__class__.__name__
        assert 0 <= seed < 1, seed
        assert isinstance(shape, tuple), shape.__class__.__name__
        assert len(shape) == 2, shape
        assert all(isinstance(s, numbers.Integral) and s > 0 for s in shape)

        # declaration
        self._seed = float(seed)
        self._height, self._width = int(shape[0]), int(shape[1])

        # delegation
        super().__init__([_StreamVideoNoiseUniform(self)])

    @classmethod
    def default(cls):
        return cls(0)

    def getstate(self) -> dict:
        return {
            "seed": self.seed,
            "shape": list(self.shape),
        }

    @property
    def seed(self):
        """
        ** The value of the seed between 0 and 1. **
        """
        return self._seed

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"seed", "shape"}
        assert set(state) == keys, set(state)-keys
        GeneratorVideoNoise.__init__(self, seed=state["seed"], shape=tuple(state["shape"]))

    @property
    def shape(self) -> tuple[int, int]:
        """
        ** The vertical and horizontal (i, j) resolution of the image. **
        """
        return (self._height, self._width)


class _StreamVideoNoiseUniform(StreamVideo):
    """
    ** Random video stream where each pixel follows a uniform law. **
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: GeneratorVideoNoise):
        assert isinstance(node, GeneratorVideoNoise), node.__class__.__name__
        super().__init__(node)

    def _snapshot(self, timestamp: float) -> av.video.frame.VideoFrame:
        # random number calculation
        seed = struct.pack("dd", self.node.seed, timestamp)
        gen = np.random.default_rng(int.from_bytes(seed, byteorder="big"))
        img = gen.integers(0, 256, (self.height, self.width, 3), dtype=np.uint8, endpoint=False)

        # av frame cast
        frame = av.video.frame.VideoFrame.from_ndarray(img, format="bgr24")
        frame.time_base = fractions.Fraction(1, 300300) # ppcm 1001, 25, 30, 60
        frame.pts = round(timestamp / frame.time_base)

        return frame

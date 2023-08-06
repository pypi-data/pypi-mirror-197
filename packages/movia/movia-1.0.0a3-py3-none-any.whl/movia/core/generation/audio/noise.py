#!/usr/bin/env python3

"""
** Generate an audio noise signal. **
--------------------------------------
"""

import numbers
import random
import struct
import typing

import numpy as np

from movia.core.classes.stream import Stream
from movia.core.classes.container import ContainerInput
from movia.core.classes.stream_audio import StreamAudio



class GeneratorAudioNoise(ContainerInput):
    """
    ** Generate a pure noise audio signal. **

    Attributes
    ----------
    seed : float
        The value of the seed between 0 and 1 (readonly).

    Examples
    --------
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>> stream = GeneratorAudioNoise(0).out_streams[0]
    >>> stream.snapshot([0, 1, 2])
    array([[ 0.10066   ,  0.33006749, -0.72271419]])
    >>> stream.snapshot([1, 0.5, 0])
    array([[ 0.33006749, -0.59415133,  0.10066   ]])
    >>>
    """

    def __init__(self, seed: numbers.Real=None):
        """
        Parameters
        ----------
        seed : numbers.Real
            The random seed to have a repeatability.
            The value must be between 0 included and 1 excluded.
            If not provided, the seed is chosen randomly.
        """
        # check
        if seed is None:
            seed = random.random()
        assert isinstance(seed, numbers.Real), seed.__class__.__name__
        assert 0 <= seed < 1, seed

        # declaration
        self._seed = float(seed)

        # delegation
        super().__init__([_StreamAudioNoiseUniform(self)])

    @classmethod
    def default(cls):
        return cls(0)

    def getstate(self) -> dict:
        return {"seed": self.seed}

    @property
    def seed(self):
        """
        ** The value of the seed between 0 and 1. **
        """
        return self._seed

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"seed"}, set(state)
        GeneratorAudioNoise.__init__(self, seed=state["seed"])


class _StreamAudioNoiseUniform(StreamAudio):
    """
    ** Random audio stream where each sample follows a uniform law. **
    """

    is_time_continuous = True

    def __init__(self, node: GeneratorAudioNoise):
        """
        Parameters
        ----------
        node : movia.core.generation.audio.noise.GeneratorAudioNoise
            Simply allows to keep the graph structure.
        """
        assert isinstance(node, GeneratorAudioNoise), node.__class__.__name__
        super().__init__(node)

    def _snapshot(self, timestamp: np.ndarray[numbers.Real]) -> np.ndarray[np.float64]:
        seed = struct.pack("d", self.node.seed)
        timestamp = timestamp.astype(np.float64, copy=False)
        audio = np.fromiter(
            (random.Random(seed + struct.pack("d", t)).uniform(-1, 1) for t in timestamp),
            dtype=np.float64,
            count=len(timestamp),
        )
        audio.resize((1, len(timestamp))) # inplace
        return audio

    @property
    def channels(self) -> int:
        return 1

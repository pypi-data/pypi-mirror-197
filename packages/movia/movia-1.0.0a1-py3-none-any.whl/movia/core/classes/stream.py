#!/usr/bin/env python3

"""
** Defines the structure of an abstract multimedia stream. **
-------------------------------------------------------------
"""


import abc
import math
import numbers



class Stream(abc.ABC):
    """
    Attributes
    ----------
    beginning : numbers.Real
        The stream beginning instant in second (readonly).
    duration : numbers.Real
        The duration of the flow in seconds, it can be infinite (readonly).
        This value needs to be accurate.
    index : int
        The stream index from the parent node (0 to n-1) (readonly).
    is_time_continuous : boolean
        True if the data is continuous in the time domain, False if it is discrete (readonly).
    node : movia.core.classes.node.Node
        The node where this stream comes from (readonly).
        Allows back propagation in the assembly graph.
    """

    def __init__(self, node):
        """
        Parameters
        ----------
        node : movia.core.classes.node.Node
            The node where this stream comes from.
            The audit must be conducted in the children's classes.
            It is not done here in order to avoid cyclic imports.
        """
        self._node = node

    def __eq__(self, other) -> bool:
        """
        ** 2 streams are equivalent if their parent nodes are similar. **
        """
        if self.__class__ != other.__class__:
            return False
        if self.index != other.index:
            return False
        if self.node != other.node:
            return False
        return True

    def __reduce__(self):
        """
        ** Allow ``pickle`` to serialize efficiently. **

        You can't just use ``__getstate__`` and ``__setstate__``
        because we don't want to duplicate the stream.
        This allows to retrieve the equivalent stream generated in the parent node.
        """
        return Stream._stream_from_parent_node, (self.node, self.index)

    @staticmethod
    def _stream_from_parent_node(node, index):
        """
        ** Return the equivalent stream contained in the parent node. **
        """
        return node.out_streams[index]

    @property
    def beginning(self) -> numbers.Real:
        """
        ** The stream beginning instant in second. **
        """
        return 0

    @property
    def duration(self) -> numbers.Real:
        """
        ** Default infinite flow duration, can be overwritten. **
        """
        return math.inf

    @property
    def index(self) -> int:
        """
        ** The stream index from the parent node (0 to n-1). **
        """
        indexs = [index for index, stream in enumerate(self.node.out_streams) if stream is self]
        if len(indexs) != 1:
            raise AttributeError(f"the node {self.node} not contains the stream {self}")
        return indexs.pop()

    @property
    @abc.abstractmethod
    def is_time_continuous(self) -> bool:
        """
        ** True if the data is continuous in the time domain, False if it is discrete. **
        """
        raise NotImplementedError

    @property
    def node(self):
        """
        ** The node where this stream comes from. **
        """
        return self._node

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """
        ** The type of stream, 'audio', 'subtitle' or 'video'. **
        """
        raise NotImplementedError


class StreamWrapper(Stream):
    """
    ** Allows to dynamically transfer the methods of an instanced stream. **

    Attribute
    ---------
    stream : movia.core.classes.stream.Stream
        The stream containing the properties to be transferred (readonly).
        This stream is one of the input streams of the parent node.
    """

    def __init__(self, node, index: numbers.Integral):
        """
        Parameters
        ----------
        node : movia.core.classes.node.Node
            The parent node, transmitted to ``movia.core.classes.stream.Stream``.
        index : number.Integral
            The index of the stream among all the input streams of the ``node``.
            0 for the first, 1 for the second ...
        """
        super().__init__(node)
        assert isinstance(index, numbers.Integral) and index >= 0, index
        assert len(node.in_streams) > index, f"only {len(node.in_streams)} streams, no {index}"
        self._index = int(index)

    @property
    def duration(self) -> numbers.Real:
        return self.stream.duration

    @property
    def index(self) -> int:
        """
        ** The stream index from the parent node (0 to n-1). **
        """
        return self._index

    @property
    def is_time_continuous(self) -> bool:
        return self.stream.is_time_continuous

    @property
    def stream(self) -> Stream:
        """
        ** The audio stream containing the properties to be transferred. **
        """
        return self.node.in_streams[self.index]

    @property
    def type(self) -> str:
        return self.stream.type

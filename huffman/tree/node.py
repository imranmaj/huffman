from .bits import Bits

from typing import Optional
from functools import total_ordering


@total_ordering
class Node:
    """
    A node in the Huffman tree
    """

    def __init__(self, value: bytes=None):
        """
        value - the value of the node
        """

        self.value = value
        self.code = None
        if self.is_leaf:
            self._frequency = 1
        else:
            self._frequency = None

        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

    def increment(self):
        """
        Increments the frequency of the node by 1
        """

        self._frequency += 1

    @property
    def frequency(self) -> int:
        """
        Returns the frequency of the value of the node
            in the file
        """

        if self._frequency is not None:
            return self._frequency
        else:
            total = 0
            if self.left is not None:
                total += self.left.frequency
            if self.right is not None:
                total += self.right.frequency
            
            return total

    @property
    def is_leaf(self) -> bool:
        """
        Returns whether the node is a leaf
        """

        return self.value is not None

    @property
    def has_left(self) -> bool:
        """
        Returns whether the node has a left child node
        """

        return self.left is not None

    @property
    def has_right(self) -> bool:
        """
        Returns whether the node has a right child node
        """

        return self.right is not None

    def __eq__(self, other: "Node") -> bool:
        return self.frequency == other.frequency

    def __lt__(self, other: "Node") -> bool:
        return self.frequency < other.frequency

    def __repr__(self) -> str:
        if self.is_leaf:
            return f"<Leaf Node value={self.value} frequency={self.frequency} code={self.code}>"
        else:
            return f"<Parent Node left={self.has_left} right={self.has_right} frequency={self.frequency}>"
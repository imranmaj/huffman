from typing import Iterator

from .bits import Bits
from .node import Node
from .exceptions import LeafNotFoundError


class LeafCollection:
    """
    A collection of leaf nodes in a Huffman tree
    """

    def __init__(self):
        self.leaves = list()

    def add_leaf(self, leaf: Node):
        """
        Adds a leaf to the collection
        """

        self.leaves.append(leaf)

    def get_leaf_by_value(self, value: bytes) -> Node:
        """
        Returns a leaf given a value to search for

        value - the value to search for
        """

        for leaf in self:
            if leaf.value == value:
                return leaf

        raise LeafNotFoundError

    def get_leaf_by_code(self, code: Bits) -> Node:
        """
        Returns a leaf given a prefix code to search for

        code - the prefix code to search for
        """

        for leaf in self:
            if leaf.code == code:
                return leaf

        raise LeafNotFoundError

    def __iter__(self) -> Iterator[Node]:
        return iter(self.leaves)

    def __len__(self) -> int:
        return len(self.leaves)

    def __repr__(self) -> str:
        return f"<LeafCollection leaves={len(self)}>"
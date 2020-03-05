from queue import PriorityQueue
from typing import BinaryIO, Iterator, Tuple

from .node import Node
from .exceptions import NodeNotFoundError, TreeNotMadeError
from .bits import Bit, Bits


class Tree:
    """
    A Huffman tree
    """

    def __init__(self):
        self.nodes = list()
        self._root = None

    def add_node(self, node: Node):
        """
        Add a node to the tree
        
        node - the node to add
        """

        try:
            existing_node = self.get_node_by_value(node.value)
        except NodeNotFoundError:
            self.nodes.append(node)
        else:
            existing_node.increment()

    def get_node_by_value(self, value: bytes) -> Node:
        """
        Returns a node given a value to search for

        value - value to search for
        """

        for node in self.nodes:
            if node.value == value:
                return node

        raise NodeNotFoundError

    @property
    def root(self) -> Node:
        """
        Returns the root node of the tree
        """

        if self._root:
            return self._root
        else:
            raise TreeNotMadeError

    def leaves(self) -> Iterator[Node]:
        """
        Returns an iterator over the leaves of the tree
        """

        bits = Bits()
        yield from self._leaves(self.root, bits)

    def _leaves(self, node: Node, bits: Bits) -> Iterator[Node]:
        """
        Recursively finds leaves of the tree

        node - node to start searching from
        bits - beginning code to assign to leaves
            (the code so far from the parent node)
        """

        if node.is_leaf:
            node.code = bits.copy()
            yield node
        else:
            if node.has_left:
                yield from self._leaves(node.left, bits + Bit(0))
            if node.has_left:
                yield from self._leaves(node.right, bits + Bit(1))

    def make(self):
        """
        Constructs the Huffman tree
        """

        q = PriorityQueue()
        for n in self.nodes:
            q.put(n)

        while q.qsize() > 1:
            parent = Node()
            parent.left = q.get()
            parent.right = q.get()
            q.put(parent)

        self._root = q.get()

    @classmethod
    def from_bytes(cls, file: bytes) -> "Tree":
        """
        Returns a tree constructed from bytes

        file - bytes to construct tree with
        """

        tree = cls()
        for byte in file:
            tree.add_node(Node(bytes([byte])))
        return tree

    def __iadd__(self, other: Node) -> "Tree":
        if not isinstance(other, Node):
            return NotImplemented
        self.add_node(other)
        return self

    def __repr__(self) -> str:
        return f"<Tree nodes={len(self.nodes)} made={self._root is not None}>"
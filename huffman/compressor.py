from .tree import Tree, LeafCollection, Bit, Bits


class Compressor:
    """
    Compresses a file

    Compression format:

    In the key for the encoded data, the first byte is an int with the number of
        byte and prefix pairs.
    Each byte and prefix code pair begins with the byte itself. 
    The byte following the byte to encode itself is an int containing the number of zeroes
        prefixing the prefix code.
    The following bytes contain the prefix code for the byte. The first bit of each of these bytes:
        0 - last 7 bits are part of prefix code, next byte is also part of prefix code
        1 - last 7 bits are part of prefix code, this is the last byte
            containing this prefix code

    Following the byte, the first byte is an int with the number of zeroes prefixing the content.
    Encoded data content immediately follows this
    """

    def __init__(self, tree: Tree, file: bytes):
        """
        tree - the Huffman tree to compress with
        file - the fiel to compress using the tree
        """

        self.leaves = LeafCollection()
        for leaf in tree.leaves():
            self.leaves.add_leaf(leaf)
        self.file = file

    def compress(self) -> bytearray:
        """
        Compresses a file
        """

        result = bytearray()
        result.extend(self._key)
        result.extend(self._content)
        return result

    @property
    def _key(self) -> bytearray:
        """
        Returns a bytearray of the key for the compressed file
            (maps real bytes to prefix codes)
        """

        key = Bits()
        # number of byte/prefix pairs
        key += Bits.from_bytes(bytes([len(self.leaves)]))

        for leaf in self.leaves:

            # byte itself
            key += Bits.from_bytes(leaf.value)

            # number of zeroes prefixing the prefix code
            leaf_code = leaf.code.copy()
            num_zeroes = leaf_code.add_zeroes_prefix(7)
            key += Bits.from_bytes(bytes([num_zeroes]))

            # prefix code
            num_bytes = len(leaf_code) // 7
            for i in range(num_bytes):
                if i == num_bytes - 1:
                    key += Bit(1)
                else:
                    key += Bit(0)
                key += leaf_code[i * 7:(i + 1) * 7]

        return key.as_bytes()

    @property
    def _content(self) -> bytearray:
        """
        Returns a bytearray that is the compressed
            content of the file
        """

        content = Bits()
        # encoded data
        for byte in self.file:
            content += self.leaves.get_leaf_by_value(bytes([byte])).code

        # number of zeroes prefixing content
        num_zeroes = content.add_zeroes_prefix(8)
        num_zeroes_byte = Bits.from_bytes(bytes([num_zeroes]))
        content = num_zeroes_byte + content

        return content.as_bytes()
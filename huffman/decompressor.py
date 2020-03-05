from .tree import Bit, Bits, LeafCollection, Node, LeafNotFoundError


class Decompressor:
    """
    Decompresses a file
    """

    def __init__(self, file: bytes):
        """
        file - the file to compress
        """

        self.file = file

    def decompress(self) -> bytearray:
        """
        Decompresses a file

        Returns a bytearray of the decompressed file
        """

        # get key
        num_codes = self.file[0]

        byte_count = 0
        prefix_count = 0
        leaves = LeafCollection()
        current_leaf = None
        current_code = Bits()
        num_zeroes = None

        for byte in Bits.from_bytes(self.file[1:]).byte_iter():
            if prefix_count == num_codes:
                # got all codes
                break

            byte_count += 1

            if current_leaf is None:
                # real byte value
                current_leaf = Node(bytes(byte.as_bytes()))
                continue
            
            if num_zeroes is None:
                # number of zeroes prefixing the prefix code
                num_zeroes = byte.as_int()
                continue

            # prefix code for byte
            current_code += byte[1:]
            if byte[0] == Bit(0):
                # get next part of prefix code
                continue

            # save found leaf
            current_leaf.code = current_code[num_zeroes:]
            leaves.add_leaf(current_leaf)

            prefix_count += 1
            current_leaf = None
            current_code = Bits()
            num_zeroes = None

        # get content
        decoded = bytearray()
        num_zeroes = self.file[byte_count + 1]
        current_code = Bits()
        for bit in Bits.from_bytes(self.file[byte_count + 2:])[num_zeroes:]:
            current_code += bit
            try:
                leaf = leaves.get_leaf_by_code(current_code)
            except LeafNotFoundError:
                continue
            else:
                decoded.append(int.from_bytes(leaf.value, "little"))
                current_code = Bits()

        return decoded
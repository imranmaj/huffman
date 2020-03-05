from typing import Iterator, Union, Iterable

from .bit import Bit


class Bits:
    """
    A sequence of bits
    """

    def __init__(self):
        self.bits = list()

    def as_bytes(self) -> bytearray:
        """
        Returns the sequence of bits as a bytearray

        Full bytes are prioritized on the right
        """

        barray = bytearray()
        current_byte = 0
        for i, bit in enumerate(self.bits):
            if i % 8 == 0 and i > 0:
                barray.append(current_byte)
                current_byte = 0
            current_byte += bit << 7 - i % 8
        barray.append(current_byte)

        return barray

    def as_int(self) -> int:
        """
        Returns the bit sequence as a single integer
        """

        total = 0
        for i, bit in enumerate(self):
            total += bit << len(self) - 1 - i
        return total

    def add_zeroes_prefix(self, partition_size) -> int:
        """
        Prepends the bit sequence with bits of value 0 until 
            the length of the sequenceis a multiple of partition_size

        partition_size - the size which the returned sequence must be a multiple of
        """

        prefixed_zeroes = type(self)()
        num_zeroes = (partition_size - len(self)) % partition_size
        for i in range(num_zeroes):
            prefixed_zeroes += Bit(0)
        prefixed_zeroes.bits += self.bits
        self.bits = prefixed_zeroes.bits
        return num_zeroes
    
    @classmethod
    def from_bytes(cls, barray: bytes) -> "Bits":
        """
        Creates a Bits object from bytes

        barray - a bytes-like object to construct the Bits object from
        """

        bits = cls()
        for byte in barray:
            for i in range(8):
                bits += Bit((byte >> 7 - i) & 1)
        return bits

    def copy(self) -> "Bits":
        """
        Creates a deep copy of the bits sequence
        """

        new_bits = type(self)()
        for bit in self:
            new_bits += Bit(bit.value)
        return new_bits

    def byte_iter(self) -> Iterator["Bits"]:
        """
        Returns an iterator over bytes in this Bits sequence
            (each byte is another Bits object of length 8)
        """

        current_byte = type(self)()
        for i, bit in enumerate(self):
            if i % 8 == 0 and i > 0:
                yield current_byte
                current_byte = type(self)()
            current_byte += Bit(bit.value)
        yield current_byte

    def __iadd__(self, other: Union[Bit, "Bits"]) -> "Bits":
        if isinstance(other, Bit):
            self.bits.append(other)
        elif isinstance(other, type(self)):
            self.bits.extend(other.bits)
        else:
            return NotImplemented

        return self

    def __add__(self, other: Union[Bit, "Bits"]) -> "Bits":
        new_bits = self.copy()
        if isinstance(other, Bit):
            new_bits.bits.append(other)
        elif isinstance(other, type(self)):
            new_bits.bits.extend(other.bits)
        else:
            return NotImplemented

        return new_bits

    def __getitem__(self, loc: Union[int, slice]) -> Union[Bit, "Bits"]:
        if isinstance(loc, int):
            return self.bits[loc]
        elif isinstance(loc, slice):
            sliced_bits = self.bits[loc]
            new_bits = type(self)()
            for bit in sliced_bits:
                new_bits += bit
            return new_bits
        else:
            return NotImplemented

    def __len__(self) -> int:
        return len(self.bits)
    
    def __eq__(self, other: "Bits") -> bool:
        return self.bits == other.bits

    def __str__(self) -> str:
        return "".join([str(bit) for bit in self])

    def __iter__(self) -> Iterator[Bit]:
        return iter(self.bits)
from typing import Literal


class Bit:
    """
    A single bit
    """

    def __init__(self, value: Literal[0, 1]):
        """
        value - the value of the bit (0 or 1)
        """

        self.value = value

    def __lshift__(self, places: int) -> int:
        return self.value << places

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: "Bit") -> bool:
        return self.value == other.value
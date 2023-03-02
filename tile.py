from typing import Union
from enum import Enum


class Type(Enum):
    VOLTORB = 0
    ONE = 1
    TWO = 2
    THREE = 3


class Tile:
    def __init__(self, value: Type) -> None:
        self.type: Type = value
        self.is_revealed: bool = False
        self.unrevealed_index: int = 0

    def value(self) -> int:
        return self.type.value

    def toggle_mark(self) -> int:
        self.unrevealed_index = (self.unrevealed_index + 1) % 3

    def __str__(self) -> Union[int, str]:
        if self.is_revealed:
            return " X" if self.type == Type.VOLTORB else f"{self.value():2}"
        else:
            return [" -", " o", "  "][self.unrevealed_index]

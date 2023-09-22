from __future__ import annotations
from variables import ALOWED_COLORS


class AbsFigure:
    _NAME: str | None = None

    def __new__(cls, color: str, y: int, x: int):
        if cls is AbsFigure:
            raise Exception("Can't create obj of abstract class")
        else:
            return object.__new__(cls)

    def __init__(self, color: str, y: int, x: int) -> None:
        self._doShah: bool
        self._avblCellsForMove: list[tuple[int, int]]
        self._avblCellsForEat: list[tuple[int, int]]
        self._color: str
        self._y: int
        self._x: int

        self._doShah = False
        self._avblCellsForMove = []
        self._avblCellsForEat = []
        self._y = y
        self._x = x
        if color in ALOWED_COLORS:
            self._color = color
        else:
            raise Exception(f"Invalid color: {color}")

    def __repr__(self) -> str:
        return f"{self._NAME}{self._color}"

    def getColor(self) -> str:
        return self._color

    def setNewCoords(self, y: int, x: int) -> None:
        self._y = y
        self._x = x

    def getAvblCellsForMove(self) -> list[tuple[int, int]]:
        return self._avblCellsForMove

    def getAvblCellsForEat(self) -> list[tuple[int, int]]:
        return self._avblCellsForEat

    def resetState(self) -> None:
        self._avblCellsForMove.clear()
        self._avblCellsForEat.clear()
        self._doShah = False

    def calcAvblCells(self, field: list[list[AbsFigure | None]]) -> None:
        raise NotImplementedError

    def toJson(self) -> dict[str, str | int | bool]:
        raise NotImplementedError

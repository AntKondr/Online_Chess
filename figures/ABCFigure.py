from __future__ import annotations
from enums import Color


class ABCFigure:
    _NAME: str

    def __new__(cls, color: Color, y: int, x: int):
        if cls is ABCFigure:
            raise Exception("Can't create obj of abstract class")
        else:
            return object.__new__(cls)

    def __init__(self, color: Color, y: int, x: int) -> None:
        # self._doShah - делает ли фигура шах
        self._doShah: bool

        # self._wasCalc - были ли вычислены доступные ходы
        self._wasCalc: bool

        # self._covered - прикрыта ли фигура союзной фигурой
        # (для того, чтоб недопустить срубание этой фигуры королём)
        self._covered: bool

        # self._coversKing - прикрывает ли фигура короля
        self._coversKing: bool

        self._avblCellsForMove: list[tuple[int, int]]
        self._avblCellsForEat: list[tuple[int, int]]
        self._color: Color
        self._y: int
        self._x: int
        self._reprColor: str

        self._doShah = False
        self._wasCalc = False
        self._covered = False
        self._coversKing = False
        self._avblCellsForMove = []
        self._avblCellsForEat = []
        self._color = color
        self._y = y
        self._x = x

        if color == Color.WHITE:
            self._reprColor = "w"
        else:
            self._reprColor = "b"

    def __repr__(self) -> str:
        return f"{self._NAME}{self._reprColor}"

    def getColor(self) -> Color:
        return self._color

    def getCoords(self) -> tuple[int, int]:
        return (self._y, self._x)

    def wasCalc(self) -> bool:
        return self._wasCalc

    def setNewCoords(self, newY: int, newX: int) -> None:
        self._y = newY
        self._x = newX

    def getControlledCells(self) -> list[tuple[int, int]]:
        return self._avblCellsForMove

    def getAvblCellsForMove(self) -> list[tuple[int, int]]:
        return self._avblCellsForMove

    def getAvblCellsForEat(self) -> list[tuple[int, int]]:
        return self._avblCellsForEat

    def clearState(self) -> None:
        self._avblCellsForMove.clear()
        self._avblCellsForEat.clear()
        self._doShah = False
        self._wasCalc = False
        self._covered = False
        self._coversKing = False

    def calcAvblCells(self, field: list[list[ABCFigure | None]]) -> None:
        raise NotImplementedError

    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[ABCFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]) -> None:
        raise NotImplementedError

    def toJson(self) -> dict[str, Color | str | int | bool]:
        raise NotImplementedError

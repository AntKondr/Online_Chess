from __future__ import annotations
from enums import Color
from .ABCFigure import ABCFigure


class King(ABCFigure):
    # король: king
    _NAME: str = "кр"
    __MOVES: tuple[tuple[int, int], ...] = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1))

    def __init__(self, color: Color, y: int, x: int) -> None:
        ABCFigure.__init__(self, color, y, x)

        self.__enemyKing: King
        self.__wasMoved: bool
        self.underShah: bool
        self.shahAmt: int
        self.__shahDirections: list[tuple[int, int]]

        self.__wasMoved = False
        self.underShah = False
        self.shahAmt = 0
        self.__shahDirections = []

    # overrided
    def setNewCoords(self, newY: int, newX: int) -> None:
        self._y = newY
        self._x = newX
        if not self.__wasMoved:
            self.__wasMoved = True

    def setEnemyKing(self, enemyKing: King) -> None:
        self.__enemyKing = enemyKing

    def getAroundCoords(self) -> list[tuple[int, int]]:
        aroundCoords: list[tuple[int, int]] = []
        for yMove, xMove in King.__MOVES:
            yt = self._y + yMove
            xt = self._x + xMove
            if (-1 < yt < 8) and (-1 < xt < 8):
                aroundCoords.append((yt, xt))
        return aroundCoords

    # overrided
    def clearState(self) -> None:
        self._avblCellsForMove.clear()
        self._avblCellsForEat.clear()
        self.__shahDirections.clear()
        self.underShah = False
        self.shahAmt = 0

    # overrided
    def calcAvblCells(self, field: list[list[ABCFigure | None]]) -> None:
        fig: ABCFigure | None
        yt: int
        xt: int
        cellsUnderAttack: set[tuple[int, int]] = set()

        for row in field:
            for fig in row:
                if not (fig is None) and (fig._color != self._color) and not (type(fig) is King):
                    if not fig._wasCalc:
                        fig.calcAvblCells(field)
                    for coord in fig.getControlledCells():
                        cellsUnderAttack.add(coord)

        for coord in self.__enemyKing.getAroundCoords():
            cellsUnderAttack.add(coord)

        for yMove, xMove in King.__MOVES:
            yt = self._y + yMove
            xt = self._x + xMove
            if (-1 < yt < 8) and (-1 < xt < 8) and (not ((yt, xt) in cellsUnderAttack)) and (not ((yMove, xMove) in self.__shahDirections)):
                fig = field[yt][xt]
                if fig is None:
                    self._avblCellsForMove.append((yt, xt))
                else:
                    if fig._color != self._color:
                        if not fig._covered:
                            self._avblCellsForEat.append((yt, xt))
                    else:
                        fig._covered = True

    def addShahDirection(self, direction: tuple[int, int]) -> None:
        self.__shahDirections.append(direction)

    # overrided
    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[ABCFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]) -> None:
        pass

    # overrided
    def toJson(self) -> dict[str, Color | str | int | bool]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

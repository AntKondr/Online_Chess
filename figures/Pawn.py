from .AbsFigure import AbsFigure
from .King import King
from variables import ALOWED_COLORS


class Pawn(AbsFigure):
    # пешка: pawn
    _NAME: str = "пш"

    def __init__(self, color: str, y: int, x: int) -> None:
        AbsFigure.__init__(self, color, y, x)

        self.__yMove: int
        self.__eatCells: tuple[tuple[int, int], tuple[int, int]]
        self.__wasMoved: bool

        self.__wasMoved = False
        if color == ALOWED_COLORS[0]:
            self.__yMove = 1
            self.__eatCells = ((1, -1), (1, 1))
        else:
            self.__yMove = -1
            self.__eatCells = ((-1, -1), (-1, 1))

    # overrided
    def setNewCoords(self, y: int, x: int) -> None:
        self._y = y
        self._x = x
        if not self.__wasMoved:
            self.__wasMoved = True

    def calcAvblCells(self, field: list[list[AbsFigure | None]]) -> None:
        yt: int
        xt: int
        fig: AbsFigure | None

        if self.__wasMoved:
            yt = self._y + self.__yMove
            if (-1 < yt < 8) and (field[yt][self._x] is None):
                self._avblCellsForMove.append((yt, self._x))
        else:
            yt = self._y
            for _ in range(2):
                yt += self.__yMove
                if (-1 < yt < 8):
                    if not (field[yt][self._x] is None):
                        break
                    self._avblCellsForMove.append((yt, self._x))

        for ym, xm in self.__eatCells:
            yt = self._y + ym
            xt = self._x + xm
            if (-1 < yt < 8) and (-1 < xt < 8):
                fig = field[yt][xt]
                if not (fig is None) and fig._color != self._color:
                    self._avblCellsForEat.append((yt, xt))
                    if type(fig) is King:
                        self._doShah = True

    def toJson(self) -> dict[str, str | int | bool]:
        return {"code": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x,
                "wasMoved": self.__wasMoved}

from enums import Color
from .AbsFigure import AbsFigure
from .King import King


class Pawn(AbsFigure):
    # пешка: pawn
    _NAME: str = "пш"

    def __init__(self, color: Color, y: int, x: int) -> None:
        AbsFigure.__init__(self, color, y, x)

        self.__wasMoved: bool
        self.__canBeTakenOnPass: bool
        self.__yMove: tuple[int, int]
        self.__eatCells: tuple[tuple[int, int], tuple[int, int]]

        self.__wasMoved = False
        self.__canBeTakenOnPass = False
        if color == Color.WHITE:
            self.__yMove = (1, 0)
            self.__eatCells = ((1, -1), (1, 1))
        else:
            self.__yMove = (-1, 0)
            self.__eatCells = ((-1, -1), (-1, 1))

    # overrided
    def setNewCoords(self, newY: int, newX: int) -> None:
        if abs(newY - self._y) == 2:
            self.__canBeTakenOnPass = True
        self._y = newY
        self._x = newX
        if not self.__wasMoved:
            self.__wasMoved = True

    def isCanBeTakenOnPass(self) -> bool:
        return self.__canBeTakenOnPass

    def setFlagTakenOnPassToFalse(self) -> None:
        self.__canBeTakenOnPass = False

    # overrided
    def calcAvblCells(self, field: list[list[AbsFigure | None]]) -> None:
        self.__calcAvblCellsForMove(field)
        self.__calcAvblCellsForEat(field)
        self._wasCalc = True

    # overrided
    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[AbsFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]
                                  ) -> None:
        for dir in directions:
            if dir == self.__yMove:
                self.__calcAvblCellsForMove(field)
            if dir in self.__eatCells:
                yt = self._y + dir[0]
                xt = self._x + dir[1]
                if (-1 < yt < 8) and (-1 < xt < 8):
                    fig = field[yt][xt]
                    if not (fig is None):
                        if fig._color != self._color:
                            self._avblCellsForEat.append((yt, xt))
                            if type(fig) is King:
                                self._doShah = True
                        else:
                            fig._covered = True
        self._wasCalc = True

    def __calcAvblCellsForMove(self, field: list[list[AbsFigure | None]]) -> None:
        yt: int

        if self.__wasMoved:
            yt = self._y + self.__yMove[0]
            if (-1 < yt < 8) and (field[yt][self._x] is None):
                self._avblCellsForMove.append((yt, self._x))
        else:
            yt = self._y
            for _ in range(2):
                yt += self.__yMove[0]
                if (-1 < yt < 8):
                    if not (field[yt][self._x] is None):
                        break
                    self._avblCellsForMove.append((yt, self._x))

    def __calcAvblCellsForEat(self, field: list[list[AbsFigure | None]]) -> None:
        yt: int
        xt: int
        fig: AbsFigure | None

        for ym, xm in self.__eatCells:
            yt = self._y + ym
            xt = self._x + xm
            if (-1 < yt < 8) and (-1 < xt < 8):
                fig = field[yt][xt]
                if not (fig is None):
                    if fig._color != self._color:
                        self._avblCellsForEat.append((yt, xt))
                        if type(fig) is King:
                            self._doShah = True
                    else:
                        fig._covered = True
                else:
                    fig = field[self._y][xt]
                    if not (fig is None) and (type(fig) is Pawn) and self._color != fig._color and fig.__canBeTakenOnPass:
                        self._avblCellsForEat.append((yt, xt))

    # overrided
    def getControlledCells(self) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for ym, xm in self.__eatCells:
            yt = self._y + ym
            xt = self._x + xm
            result.append((yt, xt))
        return result

    # overrided
    def toJson(self) -> dict[str, str | Color | int | bool]:
        return {"code": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x,
                "wasMoved": self.__wasMoved}

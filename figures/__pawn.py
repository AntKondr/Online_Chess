from enums import Color
from .__ABCFigure import ABCFigure
from .__king import King


class Pawn(ABCFigure):
    # пешка: pawn
    _NAME: str = "пш"

    def __init__(self, color: Color, y: int, x: int) -> None:
        ABCFigure.__init__(self, color, y, x)

        self.__wasMoved: bool
        self.__canBeTakenOnPass: bool
        self.__canBeConverted: bool
        self.__itWasTakeOnPass: bool
        self.__coordsOfPawnForTakenOnPass: tuple[int, int] | None
        self.__yMove: tuple[int, int]
        self.__eatCells: tuple[tuple[int, int], tuple[int, int]]
        self.__oppositeEdgeY: int

        self.__wasMoved = False
        self.__canBeTakenOnPass = False
        self.__canBeConverted = False
        self.__itWasTakeOnPass = False
        self.__coordsOfPawnForTakenOnPass = None
        if color == Color.WHITE:
            self.__yMove = (1, 0)
            self.__eatCells = ((1, -1), (1, 1))
            self.__oppositeEdgeY = 7
        else:
            self.__yMove = (-1, 0)
            self.__eatCells = ((-1, -1), (-1, 1))
            self.__oppositeEdgeY = 0

    # overrided
    def setNewCoords(self, newY: int, newX: int) -> None:
        if newY == self.__oppositeEdgeY:
            self.__canBeConverted = True
        elif self.__coordsOfPawnForTakenOnPass == (newY - self.__yMove[0], newX):
            self.__itWasTakeOnPass = True
            self.__coordsOfPawnForTakenOnPass = None

        if not self.__wasMoved:
            if abs(newY - self._y) == 2:
                self.__canBeTakenOnPass = True
            self.__wasMoved = True
        self._y = newY
        self._x = newX

    def isCanBeTakenOnPass(self) -> bool:
        return self.__canBeTakenOnPass

    def setFlagCanBeTakenOnPassToFalse(self) -> None:
        self.__canBeTakenOnPass = False

    def itWasTakeOnPass(self) -> bool:
        return self.__itWasTakeOnPass

    def setFlagItWasTakeOnPassToFalse(self) -> None:
        self.__itWasTakeOnPass = False

    def isCanBeConverted(self) -> bool:
        return self.__canBeConverted

    # overrided
    def calcAvblCells(self, field: list[list[ABCFigure | None]]) -> None:
        self.__calcAvblCellsForMove(field)
        self.__calcAvblCellsForEat(field)
        self._wasCalc = True

    # overrided
    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[ABCFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]
                                  ) -> None:
        for dir in directions:
            if dir == self.__yMove:
                self.__calcAvblCellsForMove(field)
            elif dir in self.__eatCells:
                yt = self._y + dir[0]
                xt = self._x + dir[1]
                if (-1 < yt < 8) and (-1 < xt < 8):
                    fig = field[yt][xt]
                    if fig:
                        if fig._color != self._color:
                            self._avblCellsForEat.append((yt, xt))
                            if type(fig) is King:
                                self._doShah = True
                        else:
                            fig._covered = True
        self._wasCalc = True

    def __calcAvblCellsForMove(self, field: list[list[ABCFigure | None]]) -> None:
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
                    if field[yt][self._x]:
                        break
                    self._avblCellsForMove.append((yt, self._x))

    def __calcAvblCellsForEat(self, field: list[list[ABCFigure | None]]) -> None:
        yt: int
        xt: int
        fig: ABCFigure | None

        for ym, xm in self.__eatCells:
            yt = self._y + ym
            xt = self._x + xm
            if (-1 < yt < 8) and (-1 < xt < 8):
                fig = field[yt][xt]
                if fig:
                    if fig._color != self._color:
                        self._avblCellsForEat.append((yt, xt))
                        if type(fig) is King:
                            self._doShah = True
                            fig.underShah = True
                            fig.shahAmt += 1
                    else:
                        fig._covered = True
                else:
                    fig = field[self._y][xt]
                    if type(fig) is Pawn and self._color != fig._color and fig.__canBeTakenOnPass:
                        self._avblCellsForEat.append((yt, xt))
                        self.__coordsOfPawnForTakenOnPass = (fig._y, fig._x)

    # overrided
    def getControlledCells(self) -> list[tuple[int, int]]:
        yt: int
        xt: int

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

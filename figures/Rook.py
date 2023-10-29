from enums import Color
from .ABCFigure import ABCFigure
from .King import King


class Rook(ABCFigure):
    # ладья: rook
    _NAME: str = "лд"
    __MOVES: tuple[tuple[int, int], ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))

    def __init__(self, color: Color, y: int, x: int) -> None:
        ABCFigure.__init__(self, color, y, x)

        self.__wasMoved: bool

        self.__wasMoved = False

    # overrided
    def setNewCoords(self, newY: int, newX: int) -> None:
        self._y = newY
        self._x = newX
        if not self.__wasMoved:
            self.__wasMoved = True

    # TODO переписать метод как у Queen
    # overrided
    def calcAvblCells(self, field: list[list[ABCFigure | None]]) -> None:
        yNextCell: int
        xNextCell: int
        fig: ABCFigure | None

        for yMove, xMove in Rook.__MOVES:
            yNextCell = self._y
            xNextCell = self._x
            while True:
                yNextCell += yMove
                xNextCell += xMove
                if (-1 < yNextCell < 8) and (-1 < xNextCell < 8):
                    fig = field[yNextCell][xNextCell]
                    if fig is None:
                        self._avblCellsForMove.append((yNextCell, xNextCell))
                    else:
                        if fig._color != self._color:
                            self._avblCellsForEat.append((yNextCell, xNextCell))
                            if type(fig) is King:
                                self._doShah = True
                            break
                        else:
                            fig._covered = True
                            break
                else:
                    break
        self._wasCalc = True

    # overrided
    def toJson(self) -> dict[str, str | Color | int]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

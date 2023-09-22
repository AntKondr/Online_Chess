from .AbsFigure import AbsFigure


class King(AbsFigure):
    # король: king
    _NAME: str = "кр"
    __MOVES: tuple[tuple[int, int], ...] = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1))

    def __init__(self, color: str, y: int, x: int) -> None:
        AbsFigure.__init__(self, color, y, x)

        self.__wasMoved: bool
        self.underShah: bool

        self.__wasMoved = False
        self.underShah = False

    # overrided
    def setNewCoords(self, y: int, x: int) -> None:
        self._y = y
        self._x = x
        if not self.__wasMoved:
            self.__wasMoved = True

    def calcAvblCells(self, field: list[list[AbsFigure | None]]) -> None:
        fig: AbsFigure | None
        yt: int
        xt: int

        for yMove, xMove in King.__MOVES:
            yt = self._y + yMove
            xt = self._x + xMove
            if (-1 < yt < 8) and (-1 < xt < 8):
                fig = field[yt][xt]
                if fig is None:
                    self._avblCellsForMove.append((yt, xt))
                else:
                    if fig._color != self._color:
                        self._avblCellsForEat.append((yt, xt))

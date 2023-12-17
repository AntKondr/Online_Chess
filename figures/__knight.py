from enums import Color
from .__ABCFigure import ABCFigure
from .__king import King


class Knight(ABCFigure):
    # конь: knight
    _NAME: str = "кн"
    __MOVES: tuple[tuple[int, int], ...] = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2))

    # overrided
    def calcAvblCells(self, field: list[list[ABCFigure | None]]) -> None:
        fig: ABCFigure | None
        yt: int
        xt: int

        for yMove, xMove in Knight.__MOVES:
            yt = self._y + yMove
            xt = self._x + xMove
            if (-1 < yt < 8) and (-1 < xt < 8):
                fig = field[yt][xt]
                if fig is None:
                    self._avblCellsForMove.append((yt, xt))
                else:
                    if fig._color != self._color:
                        self._avblCellsForEat.append((yt, xt))
                        if type(fig) is King:
                            self._doShah = True
                            fig.underShah = True
                            fig.shahAmt += 1
                    else:
                        fig._covered = True
        self._wasCalc = True

    # overrided
    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[ABCFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]
                                  ) -> None:
        self._wasCalc = True

    # overrided
    def toJson(self) -> dict[str, str | Color | int]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

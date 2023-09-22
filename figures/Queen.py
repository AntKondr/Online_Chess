from .AbsFigure import AbsFigure
from .King import King


class Queen(AbsFigure):
    # ферзь: queen
    _NAME: str = "фр"
    __MOVES: tuple[tuple[int, int], ...] = ((1, 1), (1, -1), (-1, -1), (-1, 1), (-1, 0), (0, 1), (1, 0), (0, -1))

    def calcAvblCells(self, field: list[list[AbsFigure | None]]) -> None:
        yNextCell: int
        xNextCell: int
        fig: AbsFigure | None

        for yMove, xMove in Queen.__MOVES:
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
                            break
                else:
                    break

    def toJson(self) -> dict[str, str | int]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

from enums import Color
from .AbsFigure import AbsFigure
from .King import King


class Queen(AbsFigure):
    # ферзь: queen
    _NAME: str = "фр"
    __MOVES: tuple[tuple[int, int], ...] = ((1, 1), (1, -1), (-1, -1), (-1, 1), (-1, 0), (0, 1), (1, 0), (0, -1))

    # overrided
    def calcAvblCells(self, field: list[list[AbsFigure | None]]) -> None:
        yNextCell: int
        xNextCell: int
        fig: AbsFigure | None
        enemyFigCount: int
        enemyFigs: list[AbsFigure]

        for yMove, xMove in Queen.__MOVES:
            yNextCell = self._y
            xNextCell = self._x
            enemyFigCount = 0
            enemyFigs = []
            while True:
                yNextCell += yMove
                xNextCell += xMove
                if (-1 < yNextCell < 8) and (-1 < xNextCell < 8):
                    fig = field[yNextCell][xNextCell]
                    if fig is None:
                        if enemyFigCount == 0:
                            self._avblCellsForMove.append((yNextCell, xNextCell))
                    else:
                        if fig._color != self._color:
                            enemyFigCount += 1
                            enemyFigs.append(fig)
                            if enemyFigCount == 1:
                                self._avblCellsForEat.append((yNextCell, xNextCell))
                            if type(fig) is King:
                                if enemyFigCount == 1:
                                    self._doShah = True
                                    fig.underShah = True
                                    fig.shahAmt += 1
                                    break
                                else:
                                    enemyFigs[0].clearState()
                                    enemyFigs[0]._coversKing = True
                                    enemyFigs[0].calcAvblCellsIfCoversKing(field, ((yMove, xMove), (yMove * -1, xMove * -1)))
                                    break
                            if enemyFigCount == 2:
                                break
                        else:
                            if enemyFigCount == 0:
                                fig._covered = True
                            break
                else:
                    break
        self._wasCalc = True

    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[AbsFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]
                                  ) -> None:
        yNextCell: int
        xNextCell: int
        fig: AbsFigure | None

        for yMove, xMove in directions:
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

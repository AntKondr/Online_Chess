from .ABCFigure import ABCFigure
from .King import King


class ABCLinearFigure(ABCFigure):
    _MOVES: tuple[tuple[int, int], ...]

    # overrided
    def calcAvblCells(self, field: list[list[ABCFigure | None]]) -> None:
        yNextCell: int
        xNextCell: int
        fig: ABCFigure | None
        enemyFigCount: int
        enemyFigs: list[ABCFigure]

        for yMove, xMove in self._MOVES:
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
                                    fig.addShahDirection((yMove, xMove))
                                    fig.addShahDirection((yMove * -1, xMove * -1))
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

    # overrided
    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[ABCFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]
                                  ) -> None:
        yNextCell: int
        xNextCell: int
        fig: ABCFigure | None

        for dir in directions:
            if dir in self._MOVES:
                yMove, xMove = dir
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

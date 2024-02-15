from __future__ import annotations
from enums import Color
from .__ABCFigure import ABCFigure


class King(ABCFigure):
    # король: king
    _NAME: str = "кр"
    __MOVES: tuple[tuple[int, int], ...] = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1))
    __SHORT_CASTLING_DIR: int = -1
    __LONG_CASTLING_DIR: int = 1

    def __init__(self, color: Color, y: int, x: int) -> None:
        ABCFigure.__init__(self, color, y, x)

        self.__enemyKing: King
        self.__wasMoved: bool
        self.__underShah: bool
        self.__itWasLongCastling: bool
        self.__itWasShortCastling: bool
        self.__shahAmt: int
        self.__shahDirections: list[tuple[int, int]]
        self.__shortCastlingCells: tuple[tuple[int, int], tuple[int, int]]
        self.__longCastlingCells: tuple[tuple[int, int], tuple[int, int]]

        self.__wasMoved = False
        self.__underShah = False
        self.__itWasLongCastling = False
        self.__itWasShortCastling = False
        self.__shahAmt = 0
        self.__shahDirections = []

        self.__shortCastlingCells = ((self._y, self._x + King.__SHORT_CASTLING_DIR),
                                     (self._y, self._x + King.__SHORT_CASTLING_DIR * 2))

        self.__longCastlingCells = ((self._y, self._x + King.__LONG_CASTLING_DIR),
                                    (self._y, self._x + King.__LONG_CASTLING_DIR * 2))

    # overrided
    def setNewCoords(self, newY: int, newX: int) -> None:
        if not self.__wasMoved:
            if newX - self._x == 2:
                self.__itWasLongCastling = True
            elif newX - self._x == -2:
                self.__itWasShortCastling = True
            self.__wasMoved = True

        self._y = newY
        self._x = newX

    def itWasLongCastling(self) -> bool:
        return self.__itWasLongCastling

    def itWasShortCastling(self) -> bool:
        return self.__itWasShortCastling

    def resetItWasLongCastling(self) -> None:
        self.__itWasLongCastling = False

    def resetItWasShortCastling(self) -> None:
        self.__itWasShortCastling = False

    def setEnemyKing(self, enemyKing: King) -> None:
        self.__enemyKing = enemyKing

    def __getAroundCoords(self) -> list[tuple[int, int]]:
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
        self.__underShah = False
        self.__shahAmt = 0

    def incrShahAmt(self) -> None:
        self.__shahAmt += 1

    def setUnderShah(self) -> None:
        if not self.__underShah:
            self.__underShah = True

    # overrided
    def calcAvblCells(self, field: list[list[ABCFigure | None]]) -> None:
        fig: ABCFigure | None
        yt: int
        xt: int
        cellsUnderAttack: set[tuple[int, int]] = set()

        for row in field:
            for fig in row:
                if fig and fig._color != self._color and not (type(fig) is King):
                    if not fig._wasCalc:
                        fig.calcAvblCells(field)
                    for coord in fig.getControlledCells():
                        cellsUnderAttack.add(coord)

        for coord in self.__enemyKing.__getAroundCoords():
            cellsUnderAttack.add(coord)

        for yMove, xMove in King.__MOVES:
            yt = self._y + yMove
            xt = self._x + xMove
            if (-1 < yt < 8) and (-1 < xt < 8) and (not ((yt, xt) in cellsUnderAttack)) and (not ((yMove, xMove) in self.__shahDirections)):
                fig = field[yt][xt]
                if fig:
                    if fig._color != self._color:
                        if not fig._covered:
                            self._avblCellsForEat.append((yt, xt))
                    else:
                        fig._covered = True
                else:
                    self._avblCellsForMove.append((yt, xt))

        if not self.__wasMoved and not self.__underShah:
            shortRook: ABCFigure | None = field[self._y][0]
            longRook: ABCFigure | None = field[self._y][7]

            if shortRook and shortRook.isRookAndNotWasMoved() and \
               self.__cellsBetweenKingAndRookAreEmpty(King.__SHORT_CASTLING_DIR, field) and \
               self.__castlingCellsNotUnderAttack(King.__SHORT_CASTLING_DIR, cellsUnderAttack):
                self._avblCellsForMove.append(self.__shortCastlingCells[1])
                print(f"{self._reprColor} short castling avbl")

            if longRook and longRook.isRookAndNotWasMoved() and \
               self.__cellsBetweenKingAndRookAreEmpty(King.__LONG_CASTLING_DIR, field) and \
               self.__castlingCellsNotUnderAttack(King.__LONG_CASTLING_DIR, cellsUnderAttack):
                self._avblCellsForMove.append(self.__longCastlingCells[1])
                print(f"{self._reprColor} long castling avbl")

    def __cellsBetweenKingAndRookAreEmpty(self,
                                          CastlingDirection: int,
                                          field: list[list[ABCFigure | None]]
                                          ) -> bool:
        cell: ABCFigure | None

        nextX: int = self._x + CastlingDirection
        if CastlingDirection < 0:
            while nextX > 0:
                cell = field[self._y][nextX]
                if cell:
                    return False
                nextX += CastlingDirection
        else:
            while nextX < 7:
                cell = field[self._y][nextX]
                if cell:
                    return False
                nextX += CastlingDirection

        return True

    def __castlingCellsNotUnderAttack(self,
                                      CastlingDirection: int,
                                      cellsUnderAttack: set[tuple[int, int]]
                                      ) -> bool:
        if CastlingDirection < 0:
            for cell in self.__shortCastlingCells:
                if cell in cellsUnderAttack:
                    return False
        else:
            for cell in self.__longCastlingCells:
                if cell in cellsUnderAttack:
                    return False

        return True

    def addShahDirection(self, direction: tuple[int, int]) -> None:
        self.__shahDirections.append(direction)

    # overrided
    def calcAvblCellsIfCoversKing(self,
                                  field: list[list[ABCFigure | None]],
                                  directions: tuple[tuple[int, int], tuple[int, int]]
                                  ) -> None:
        pass

    # overrided
    def toJson(self) -> dict[str, Color | str | int | bool]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

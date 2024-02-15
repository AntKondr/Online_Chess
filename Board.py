from enums import Color
from figures import ABCFigure
from figures import King
from figures import Queen
from figures import Bishop
from figures import Rook
from figures import Knight
from figures import Pawn


class Board:
    __XCOLS: dict[str, int] = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0}
# {7: "a", 6: "b", 5: "c", 4: "d", 3: "e", 2: "f", 1: "g", 0: "h"}

    def __init__(self) -> None:
        self.whiteKing: King
        self.blackKing: King
        self.pawnThatCanBeTakenOnPass: Pawn | None
        self.__field: list[list[ABCFigure | None]]

        w: Color = Color.WHITE
        b: Color = Color.BLACK

        self.whiteKing = King(w, 0, 3)
        self.blackKing = King(b, 7, 3)
        self.whiteKing.setEnemyKing(self.blackKing)
        self.blackKing.setEnemyKing(self.whiteKing)

        self.pawnThatCanBeTakenOnPass = None

        self.__field = [[Rook(w, 0, 0), Knight(w, 0, 1), Bishop(w, 0, 2), self.whiteKing, Queen(w, 0, 4), Bishop(w, 0, 5), Knight(w, 0, 6), Rook(w, 0, 7)],
                        [Pawn(w, 1, 0), Pawn(w, 1, 1), Pawn(w, 1, 2), Pawn(w, 1, 3), Pawn(w, 1, 4), Pawn(w, 1, 5), Pawn(w, 1, 6), Pawn(w, 1, 7)],
                        [None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None, None],
                        [Pawn(b, 6, 0), Pawn(b, 6, 1), Pawn(b, 6, 2), Pawn(b, 6, 3), Pawn(b, 6, 4), Pawn(b, 6, 5), Pawn(b, 6, 6), Pawn(b, 6, 7)],
                        [Rook(b, 7, 0), Knight(b, 7, 1), Bishop(b, 7, 2), self.blackKing, Queen(b, 7, 4), Bishop(b, 7, 5), Knight(b, 7, 6), Rook(b, 7, 7)]]

    def moveFigure(self, coordsF: str, coordsT: str) -> bool:
        fig: ABCFigure | None

        xF: int = Board.__XCOLS[coordsF[0]]
        yF: int = int(coordsF[1]) - 1

        xT: int = Board.__XCOLS[coordsT[0]]
        yT: int = int(coordsT[1]) - 1

        fig = self.__field[yF][xF]

        if fig and (yT, xT) in fig.getAvblCellsForMove() + fig.getAvblCellsForEat():
            self.__field[yT][xT] = self.__field[yF][xF]
            self.__field[yF][xF] = None
            fig.setNewCoords(yT, xT)
            if type(fig) is Pawn:
                if fig.isCanBeTakenOnPass():
                    if self.pawnThatCanBeTakenOnPass:
                        self.pawnThatCanBeTakenOnPass.setFlagCanBeTakenOnPassToFalse()
                    self.pawnThatCanBeTakenOnPass = fig

                elif fig.itWasTakeOnPass() and self.pawnThatCanBeTakenOnPass:
                    y, x = self.pawnThatCanBeTakenOnPass.getCoords()
                    self.__field[y][x] = None
                    self.pawnThatCanBeTakenOnPass = None
                    fig.setFlagItWasTakeOnPassToFalse()

                elif fig.isCanBeConverted():
                    # make convertation
                    input("pawn can be converted, press enter")

            elif type(fig) is King:
                if fig.itWasLongCastling():
                    rook: ABCFigure | None = self.__field[yT][7]
                    self.__field[yT][xT - 1] = rook
                    self.__field[yT][7] = None
                    fig.resetItWasLongCastling()
                    if rook:
                        rook.setNewCoords(yT, xT - 1)
                elif fig.itWasShortCastling():
                    rook: ABCFigure | None = self.__field[yT][0]
                    self.__field[yT][xT + 1] = rook
                    self.__field[yT][0] = None
                    fig.resetItWasShortCastling()
                    if rook:
                        rook.setNewCoords(yT, xT + 1)
            return True
        return False

    def setFlagPawnWhoCanBeTakenOnPassToFalse(self, color: Color) -> None:
        if self.pawnThatCanBeTakenOnPass and self.pawnThatCanBeTakenOnPass.getColor() == color:
            self.pawnThatCanBeTakenOnPass.setFlagCanBeTakenOnPassToFalse()
            self.pawnThatCanBeTakenOnPass = None

    def clearFigsState(self) -> None:
        for row in self.__field:
            for fig in row:
                if not (fig is None):
                    fig.clearState()

    def calcFigsState(self) -> None:
        self.whiteKing.calcAvblCells(self.__field)
        self.blackKing.calcAvblCells(self.__field)

    def getFigure(self, coords: str) -> ABCFigure | None:
        # coords = f8
        x: int = Board.__XCOLS[coords[0]]
        y: int = int(coords[1]) - 1
        return self.__field[y][x]

    def checkCoords(self, coords: str, color: Color) -> bool:
        fig: ABCFigure | None

        x: int = Board.__XCOLS[coords[0]]
        y: int = int(coords[1]) - 1
        fig = self.__field[y][x]
        if (fig is None) or (fig.getColor() != color) or (len(fig.getAvblCellsForMove() + fig.getAvblCellsForEat()) == 0):
            return False
        return True

    def getField(self) -> list[list[ABCFigure | None]]:
        return self.__field

    def toJson(self) -> list[list[dict[str, str | Color | int | bool] | None]]:
        tmp: list[dict[str, str | Color | int | bool] | None]
        res: list[list[dict[str, str | Color | int | bool] | None]]

        res = []
        for row in self.__field:
            tmp = []
            for col in row:
                if col is None:
                    tmp.append(col)
                else:
                    tmp.append(col.toJson())
            res.append(tmp)
        return res

from json import dumps
from Player import Player
from Board import Board
from enums import Color


class Game:
    def __init__(self,
                 whitePlayer: Player,
                 blackPlayer: Player,
                 id: int) -> None:
        self.id: int
        self.whitePlayer: Player
        self.blackPlayer: Player
        self.activePlayer: Player
        self.unActivePlayer: Player
        self.board: Board
        self.delay: int

        self.id = id
        self.whitePlayer = whitePlayer
        self.blackPlayer = blackPlayer
        self.board = Board()
        self.delay = 0
        self.activePlayer = self.whitePlayer
        self.unActivePlayer = self.blackPlayer

    def doHod(self) -> None:
        self.board.calcFigsState()
        self.board.setFlagPawnWhoCanBeTakenOnPassToFalse(self.activePlayer.color)
        self.activePlayer.doHod(self.board)
        self.__changeActivePlayer()
        self.board.clearFigsState()

    def __changeActivePlayer(self) -> None:
        if self.activePlayer is self.whitePlayer:
            self.activePlayer = self.blackPlayer
            self.unActivePlayer = self.whitePlayer
        else:
            self.activePlayer = self.whitePlayer
            self.unActivePlayer = self.blackPlayer

    def toJson(self) -> str:
        d = {"id": self.id,
             "whitePlayer": self.whitePlayer.toJson(),
             "blackPlayer": self.blackPlayer.toJson(),
             "activePlayer": self.activePlayer.toJson(),
             "board": self.board.toJson()}
        return dumps(d, indent=4)

    def getStrRepr(self, color: Color) -> str:
        field = self.board.getField()
        divider: str = "\n   -------------------------------------------------\n"
        out: str = f"Ходит {self.activePlayer}!\n\n"
        if color == Color.WHITE:
            charsW: str = "      a     b     c     d     e     f     g     h"
            out += (charsW + divider)
            for row in range(7, -1, -1):
                out += f"{row + 1}  | "
                for col in range(7, -1, -1):
                    item = field[row][col]
                    if item is None:
                        item = "   "
                    out += f"{item} | "
                out += f" {row + 1}{divider}"
            out += charsW + "\n"
        else:
            charsB: str = "      h     g     f     e     d     c     b     a"
            out += (charsB + divider)
            for row in range(0, 8):
                out += f"{row + 1}  | "
                for col in range(0, 8):
                    item = field[row][col]
                    if item is None:
                        item = "   "
                    out += f"{item} | "
                out += f" {row + 1}{divider}"
            out += charsB + "\n"
        return out

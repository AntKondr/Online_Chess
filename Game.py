from json import dumps
from os import system
from random import randint
from Player import Player
from Board import Board


class Game:
    id: int
    whitePlayer: Player
    blackPlayer: Player

    activePlayer: Player
    board: Board
    delay: int

    def __init__(self,
                 whitePlayer: Player,
                 blackPlayer: Player,
                 id: int
                 ) -> None:
        self.whitePlayer = whitePlayer
        self.blackPlayer = blackPlayer
        self.id = id

        self.board = Board()
        self.delay = 0
        if randint(0, 1) == 0:
            self.activePlayer = self.whitePlayer
        else:
            self.activePlayer = self.blackPlayer

    def toJson(self) -> str:
        d = {"id": self.id,
             "whitePlayer": self.whitePlayer.toJson(),
             "blackPlayer": self.blackPlayer.toJson(),
             "activePlayer": self.activePlayer.toJson(),
             "board": self.board.toJson()}
        return dumps(d, indent=4)

    # TODO
    def get_starts_parameters(self) -> str:
        return "pass"

    def show_in_console(self) -> None:
        rotate180: bool
        if self.activePlayer.color == "w":
            rotate180 = True
        else:
            rotate180 = False
        field = self.board.getField()
        divider: str = "\n   -------------------------------------------------\n"
        out: str = f"Ходит {self.activePlayer}!\n\n"
        if rotate180:
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
        system("cls")
        print(out)

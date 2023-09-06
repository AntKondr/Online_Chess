from figures.Bishop import Bishop
from figures.King import King
from figures.Knight import Knight
from figures.Pawn import Pawn
from figures.Queen import Queen
from figures.Rook import Rook


class Board:
    __COLS: dict[str | int, int | str] = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0,
                                          7: "a", 6: "b", 5: "c", 4: "d", 3: "e", 2: "f", 1: "g", 0: "h"}

    def __init__(self) -> None:
        self.field = [[Rook("w", 0, 0), Knight("w", 0, 1), Bishop("w", 0, 2), King("w", 0, 3), Queen("w", 0, 4), Bishop("w", 0, 5), Knight("w", 0, 6), Rook("w", 0, 7)],
                      [Pawn("w", 1, 0), Pawn("w", 1, 1), Pawn("w", 1, 2), Pawn("w", 1, 3), Pawn("w", 1, 4), Pawn("w", 1, 5), Pawn("w", 1, 6), Pawn("w", 1, 7)],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn("b", 6, 0), Pawn("b", 6, 1), Pawn("b", 6, 2), Pawn("b", 6, 3), Pawn("b", 6, 4), Pawn("b", 6, 5), Pawn("b", 6, 6), Pawn("b", 6, 7)],
                      [Rook("b", 7, 0), Knight("b", 7, 1), Bishop("b", 7, 2), King("b", 7, 3), Queen("b", 7, 4), Bishop("b", 7, 5), Knight("b", 7, 6), Rook("b", 7, 7)]]

    def show_board_in_console(self, rotate180: bool = False) -> None:
        __DIVIDER: str = "\n   -------------------------------------------------\n"
        out: str
        if rotate180:
            __CHARS_W: str = "      a     b     c     d     e     f     g     h"
            out = __CHARS_W + __DIVIDER
            for row in range(7, -1, -1):
                out += f"{row + 1}  | "
                for col in range(7, -1, -1):
                    item = self.field[row][col]
                    if item is None:
                        item = "   "
                    out += f"{item} | "
                out += f" {row + 1}{__DIVIDER}"
            out += __CHARS_W + "\n"
            print(out)
        else:
            __CHARS_B: str = "      h     g     f     e     d     c     b     a"
            out = __CHARS_B + __DIVIDER
            for row in range(0, 8):
                out += f"{row + 1}  | "
                for col in range(0, 8):
                    item = self.field[row][col]
                    if item is None:
                        item = "   "
                    out += f"{item} | "
                out += f" {row + 1}{__DIVIDER}"
            out += __CHARS_B + "\n"
            print(out)

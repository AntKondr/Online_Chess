from .AbsFigure import AbsFigure


class Pawn(AbsFigure):
    # пешка: pawn
    _NAME: str = "пш"

    was_moved: bool
    moves: tuple[tuple[int, int], tuple[int, int]]
    eat_cells: tuple[tuple[int, int], tuple[int, int]]

    def __init__(self, color: str, y: int, x: int) -> None:
        super().__init__(color, y, x)
        self.was_moved = False
        if color == self._ALOWED_COLORS[0]:
            self.moves = ((1, 0), (2, 0))
            self.eat_cells = ((1, -1), (1, 1))
        else:
            self.moves = ((-1, 0), (-2, 0))
            self.eat_cells = ((-1, -1), (-1, 1))

    # def move(self) -> None:
    #     self.was_moved: bool = True
    #     if self.color == self._ALOWED_COLORS[0]:
    #         self.moves = (1, 0)
    #     else:
    #         self.moves = (-1, 0)

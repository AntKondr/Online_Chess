from .AbsFigure import AbsFigure


class Bishop(AbsFigure):
    # слон: bishop
    _NAME: str = "сл"

    def __init__(self, color: str, y: int, x: int) -> None:
        super().__init__(color, y, x)
        self.moves = ((1, 1), (1, -1), (-1, -1), (-1, 1))

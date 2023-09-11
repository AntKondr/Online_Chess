from .AbsFigure import AbsFigure


class Bishop(AbsFigure):
    # слон: bishop
    _NAME: str = "сл"
    isStaticFig: bool = False

    moves: tuple[tuple[int, int], ...]
    moves = ((1, 1), (1, -1), (-1, -1), (-1, 1))

    # def __init__(self, color: str, y: int, x: int) -> None:
    #     super().__init__(color, y, x)

    def toJson(self) -> dict[str, str | int]:
        return {"name": self._NAME,
                "color": self.color,
                "y": self.y,
                "x": self.x}

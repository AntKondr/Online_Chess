from enums import Color
from .ABCLinearFigure import ABCLinearFigure


class Queen(ABCLinearFigure):
    # ферзь: queen
    _NAME: str = "фр"
    _MOVES: tuple[tuple[int, int], ...] = ((1, 1), (1, -1), (-1, -1), (-1, 1), (-1, 0), (0, 1), (1, 0), (0, -1))

    # overrided
    def toJson(self) -> dict[str, str | Color | int]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

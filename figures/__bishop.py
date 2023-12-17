from enums import Color
from .__ABCLinearFigure import ABCLinearFigure


class Bishop(ABCLinearFigure):
    # слон: bishop
    _NAME: str = "сл"
    _MOVES: tuple[tuple[int, int], ...] = ((1, 1), (1, -1), (-1, -1), (-1, 1))

    # overrided
    def toJson(self) -> dict[str, str | Color | int]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

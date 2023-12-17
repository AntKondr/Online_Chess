from enums import Color
from .__ABCLinearFigure import ABCLinearFigure


class Rook(ABCLinearFigure):
    # ладья: rook
    _NAME: str = "лд"
    _MOVES: tuple[tuple[int, int], ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))

    def __init__(self, color: Color, y: int, x: int) -> None:
        ABCLinearFigure.__init__(self, color, y, x)

        self.__wasMoved: bool

        self.__wasMoved = False

    # overrided
    def setNewCoords(self, newY: int, newX: int) -> None:
        self._y = newY
        self._x = newX
        if not self.__wasMoved:
            self.__wasMoved = True

    # overrided
    def toJson(self) -> dict[str, str | Color | int]:
        return {"name": self._NAME,
                "color": self._color,
                "y": self._y,
                "x": self._x}

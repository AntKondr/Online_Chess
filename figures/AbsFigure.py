from typing import Optional


class AbsFigure:
    _NAME: Optional[str] = None
    _ALOWED_COLORS: tuple[str, str] = ("w", "b")
    color: str
    y: int
    x: int

    def __new__(cls, color: str, y: int, x: int):
        if cls is AbsFigure:
            raise Exception("Can't create obj of abstract class")
        else:
            return super().__new__(cls)

    def __init__(self, color: str, y: int, x: int) -> None:
        if color in self._ALOWED_COLORS:
            self.color = color
        else:
            raise Exception(f"Invalid color: {color}")
        self.y = y
        self.x = x

    def __str__(self) -> str:
        return f"{self._NAME}{self.color}"

    def __repr__(self) -> str:
        return f"{self._NAME}{self.color}"

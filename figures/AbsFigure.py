class AbsFigure:
    _ALOWED_COLORS: tuple[str, str] = ("w", "b")
    _NAME: str | None = None
    color: str
    y: int
    x: int

    def __new__(cls, color: str, y: int, x: int):
        if cls is AbsFigure:
            raise Exception("Can't create obj of abstract class")
        else:
            return super().__new__(cls)

    def __init__(self, color: str, y: int, x: int) -> None:
        if color in AbsFigure._ALOWED_COLORS:
            self.color = color
        else:
            raise Exception(f"Invalid color: {color}")
        self.y = y
        self.x = x

    def __repr__(self) -> str:
        return f"{self._NAME}{self.color}"

    def toJson(self) -> dict[str, str | int | bool]:
        raise NotImplementedError

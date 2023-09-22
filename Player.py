from socket import socket as Socket
from Board import Board
# from figures.AbsFigure import AbsFigure
from variables import ALOWED_COLORS


class Player:
    def __init__(self,
                 clientSocket: Socket,
                 clientAdres: tuple[str, int],
                 color: str) -> None:
        self.socket: Socket
        self.adres: tuple[str, int]
        self.request: str
        self.readyForRecv: bool
        self.color: str
        self.wasRokirovka: bool
        self.score: int

        self.socket = clientSocket
        self.adres = clientAdres
        self.request = ""
        self.readyForRecv = True
        self.wasRokirovka = False
        self.score = 0
        if color in ALOWED_COLORS:
            self.color = color
        else:
            raise Exception(f"Invalid color: {color}")

    def doHod(self, board: Board) -> None:
        coords: list[str]
        coordsF: str
        coordsT: str
        # success: bool

        coords = self.request.split()
        coordsF = coords[0]
        # success = board.checkCoords(coordsF, self.color)
        # while not success:
        #     print("там пустая клетка или вражеская фигура или фигура ничего не может сделать!")
        #     coordsF = input("введите координаты фигуры: ")
        #     success = board.checkCoords(coordsF, self.color)

        coordsT = coords[1]
        board.moveFigure(coordsF, coordsT)
        # while not success:
        #     print("недопустимые координаты")
        #     coordsT = input("куда двигаем, координаты: ")
        #     success = board.moveFigure(coordsF, coordsT)

    def __repr__(self) -> str:
        color: str
        if self.color == "w":
            color = "белый"
        else:
            color = "чёрный"
        return f"{color} игрок {self.adres}"

    def toJson(self) -> dict[str, str | bool | tuple[str, int]]:
        return {"adr": self.adres,
                "color": self.color,
                "wasRokirovka": self.wasRokirovka}

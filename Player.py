from socket import socket as Socket
from Board import Board
from enums import Color


class Player:
    def __init__(self,
                 name: str,
                 clientSocket: Socket,
                 clientAdres: tuple[str, int],
                 color: Color) -> None:
        self.name: str
        self.socket: Socket
        self.adres: tuple[str, int]
        self.request: str
        self.readyForRecv: bool
        self.wasRokirovka: bool
        self.color: Color

        self.name = name
        self.socket = clientSocket
        self.adres = clientAdres
        self.request = ""
        self.readyForRecv = True
        self.wasRokirovka = False
        self.color = color

    def doHod(self, board: Board) -> None:
        # coords: list[str]
        coordsF: str
        coordsT: str
        # success: bool
        board.setFlagPawnWhoCanBeTakenOnPassToFalse(self.color)

        # coords = self.request.split()
        # coordsF = coords[0]
        coordsF = input("введите координаты фигуры: ")
        success = board.checkCoords(coordsF, self.color)
        while not success:
            print("там пустая клетка или вражеская фигура или фигура ничего не может сделать!")
            coordsF = input("введите координаты фигуры: ")
            success = board.checkCoords(coordsF, self.color)

        # coordsT = coords[1]
        coordsT = input("куда двигаем, координаты: ")
        success = board.moveFigure(coordsF, coordsT)
        while not success:
            print("недопустимые координаты")
            coordsT = input("куда двигаем, координаты: ")
            success = board.moveFigure(coordsF, coordsT)
        board.moveFigure(coordsF, coordsT)

    def __repr__(self) -> str:
        color: str
        if self.color == Color.WHITE:
            color = "белый"
        else:
            color = "чёрный"
        return f"{color} игрок {self.name} {self.adres}"

    def toJson(self) -> dict[str, str | Color | bool | tuple[str, int]]:
        return {"name": self.name,
                "adr": self.adres,
                "color": self.color,
                "wasRokirovka": self.wasRokirovka}

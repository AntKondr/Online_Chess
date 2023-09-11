from socket import socket as Socket


class Player:
    socket: Socket
    adres: str
    request: str | None

    color: str
    wasRokirovka: bool
    score: int

    def __init__(self,
                 clientSocket: Socket,
                 clientAdres: str,
                 color: str) -> None:
        self.socket = clientSocket
        self.adres = clientAdres
        self.request = None
        self.color = color
        self.wasRokirovka = False
        self.score = 0

    def __repr__(self) -> str:
        color: str
        if self.color == "w":
            color = "белый"
        else:
            color = "чёрный"
        return f"{color} игрок {self.adres}"

    def toJson(self) -> dict[str, str]:
        return {"adr": self.adres,
                "color": self.color}

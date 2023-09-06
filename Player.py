from typing import Optional
from socket import socket as Socket


class Player:
    socket: Socket
    adres: str
    color: str
    request: Optional[str]
    score: int

    def __init__(self,
                 client_socket: Socket,
                 client_adres: str,
                 color: str) -> None:
        self.socket = client_socket
        self.adres = client_adres
        self.color = color
        self.request = None
        self.score = 0

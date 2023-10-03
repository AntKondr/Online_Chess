from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from os import system


system("cls")
ALLOWED_IP: tuple[str, ...] = ("127.0.0.1", "192.168.43.201", "192.168.1.107", "93.183.72.52")

name: str
clientSocket: Socket

name = input("Введи своё имя: ")
clientSocket = Socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
clientSocket.connect((ALLOWED_IP[0], 8000))
clientSocket.send(name.encode("utf-8"))

gameStrRepr: str
color: str
active: bytes
coordsF: str
coordsT: str

color = clientSocket.recv(16).decode("utf-8")
print(f"Your color: {color}\nwait for second player....")
while True:
    active = clientSocket.recv(1)
    gameStrRepr = clientSocket.recv(2048).decode("utf-8")
    system("cls")
    print(gameStrRepr)

    if active == b"\x01":
        print("Ваш ход!")
        coordsF = input("введите координаты фигуры: ")
        coordsT = input("куда двигаем, координаты: ")
        clientSocket.send(f"{coordsF} {coordsT}".encode("utf-8"))
    else:
        print("WAIT")

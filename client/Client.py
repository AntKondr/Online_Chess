from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
# from json import loads
from os import system


system("cls")
ALLOWED_IP: list[str] = ['127.0.0.1', '192.168.43.201', '192.168.1.107']

clientSocket: Socket
clientSocket = Socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
clientSocket.connect((ALLOWED_IP[0], 8000))

gameStrRepr: str
iAmActive: bool = False
color: str
active: str
coordsF: str
coordsT: str

color = clientSocket.recv(8).decode('utf-8')
print(f"Your color: {color}\nwait for second player....")
while True:
    active = clientSocket.recv(8).decode('utf-8')
    gameStrRepr = clientSocket.recv(2048).decode('utf-8')
    system("cls")
    print(gameStrRepr)

    if active == "act":
        print("Ваш ход!")
        coordsF = input("введите координаты фигуры: ")
        coordsT = input("куда двигаем, координаты: ")
        clientSocket.send(f"{coordsF} {coordsT}".encode('utf-8'))
    else:
        print("WAIT")

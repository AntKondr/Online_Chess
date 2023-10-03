from Game import Game
from Player import Player
from enums import Color
from time import sleep
from os import system
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY


system("cls")
ALLOWED_IP: tuple[str, ...] = ("127.0.0.1", "192.168.43.201", "192.168.1.107", "93.183.72.52")
serverSocket: Socket

serverSocket = Socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
serverSocket.bind((ALLOWED_IP[0], 8000))
serverSocket.setblocking(False)
serverSocket.listen()
print("Chess server started\n")

gameId: int = 1
games: list[Game] = []
pairPlayers: list[Player] = []
run: bool = True

name: str
clientSocket: Socket
clientAdres: tuple[str, int]
color: Color
newPlayer: Player
newGame: Game

while run:
    try:
        clientSocket, clientAdres = serverSocket.accept()
        clientSocket.setblocking(False)
        name = clientSocket.recv(256).decode("utf-8")
        if len(pairPlayers) == 0:
            color = Color.WHITE
        else:
            color = Color.BLACK
        newPlayer = Player(name, clientSocket, clientAdres, color)
        print(f"{clientAdres} {name} connected")
        clientSocket.send(str(color.value).encode("utf-8"))
        pairPlayers.append(newPlayer)
    except BlockingIOError:
        pass

    if len(pairPlayers) == 2:
        newGame = Game(pairPlayers[0], pairPlayers[1], gameId)
        games.append(newGame)
        gameId += 1
        pairPlayers.clear()

    for game in games:
        if game.delay > 9:
            if game.activePlayer.readyForRecv:
                game.activePlayer.socket.send(b"\x01")
                game.activePlayer.socket.send(game.getStrRepr(game.activePlayer.color).encode("utf-8"))
                game.activePlayer.readyForRecv = False

            if game.unActivePlayer.readyForRecv:
                game.unActivePlayer.socket.send(b"\x00")
                game.unActivePlayer.socket.send(game.getStrRepr(game.unActivePlayer.color).encode("utf-8"))
                game.unActivePlayer.readyForRecv = False

            try:
                game.activePlayer.request = game.activePlayer.socket.recv(8).decode("utf-8")
                print(f"request => {game.activePlayer.request}")
                game.doHod()
                game.activePlayer.readyForRecv = True
                game.unActivePlayer.readyForRecv = True
            except BlockingIOError:
                pass
        else:
            game.delay += 1
    sleep(0.5)

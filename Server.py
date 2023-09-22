from Game import Game
from Player import Player
from variables import ALOWED_COLORS
from time import sleep
from os import system
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY


system("cls")
ALLOWED_IP: tuple[str, ...] = ('127.0.0.1', '192.168.43.201', '192.168.1.107')
serverSocket: Socket

serverSocket = Socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
serverSocket.bind((ALLOWED_IP[0], 8000))
serverSocket.setblocking(False)
serverSocket.listen()
print('Chess server started\n')

gameId: int = 1
games: list[Game] = []
pairPlayers: list[Player] = []
run: bool = True

clientSocket: Socket
clientAdres: tuple[str, int]
color: str
newPlayer: Player
newGame: Game

while run:
    try:
        clientSocket, clientAdres = serverSocket.accept()
        clientSocket.setblocking(False)
        if len(pairPlayers) == 0:
            # w
            color = ALOWED_COLORS[0]
        else:
            # b
            color = ALOWED_COLORS[1]
        newPlayer = Player(clientSocket, clientAdres, color)
        print(f"{newPlayer.adres} connected")
        newPlayer.socket.send((color).encode('utf-8'))
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
                game.activePlayer.socket.send(("act").encode('utf-8'))
                game.activePlayer.socket.send(game.getStrRepr(game.activePlayer.color).encode('utf-8'))
                game.activePlayer.readyForRecv = False

            if game.unActivePlayer.readyForRecv:
                game.unActivePlayer.socket.send(("unact").encode('utf-8'))
                game.unActivePlayer.socket.send(game.getStrRepr(game.unActivePlayer.color).encode('utf-8'))
                game.unActivePlayer.readyForRecv = False

            try:
                game.activePlayer.request = game.activePlayer.socket.recv(8).decode('utf-8')
                print('request =>', game.activePlayer.request)
                if game.activePlayer.request != "":
                    game.doHod()
                    game.activePlayer.request = ""
                    game.activePlayer.readyForRecv = True
                    game.unActivePlayer.readyForRecv = True
            except BlockingIOError:
                pass
            # try:
            #     response = game.form_response(player.request)
            #     player.socket.send(response.encode('utf-8'))
            # except AttributeError:
            #     print('ответ игроку', player.adres, 'не удалось\n')
        else:
            game.delay += 1
    sleep(0.5)

from Game import Game
from Player import Player
from time import sleep
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY


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
clientAdres: str
newPlayer: Player
newGame: Game

while run:
    try:
        clientSocket, clientAdres = serverSocket.accept()
        clientSocket.setblocking(False)
        if len(pairPlayers) == 0:
            color = "w"
        else:
            color = "b"
        newPlayer = Player(clientSocket, clientAdres, color)
        print(f"{newPlayer.adres} connected")
        newPlayer.socket.send((color).encode('utf-8'))
        pairPlayers.append(newPlayer)
    except BlockingIOError:
        pass

    if len(pairPlayers) == 2:
        new_game = Game(pairPlayers[0], pairPlayers[1], gameId)
        games.append(new_game)
        gameId += 1
        for player in pairPlayers:
            player.socket.send(new_game.get_starts_parameters().encode('utf-8'))
        pairPlayers.clear()

    for game in games:
        if game.delay > 9:
            # do game
            pass
        else:
            game.delay += 1
    sleep(0.5)

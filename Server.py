from Game import Game
from Player import Player
from time import sleep
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY


ALLOWED_IP: tuple[str, ...] = ('127.0.0.1', '192.168.43.201', '192.168.1.107')

server_socket = Socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
server_socket.bind((ALLOWED_IP[0], 8000))
server_socket.setblocking(False)
server_socket.listen()
print('Chess server started\n')

game_id: int = 1
games: list[Game] = []
pair_players: list[Player] = []
run: bool = True

client_socket: Socket
client_adres: str
new_player: Player
new_game: Game

while run:
    try:
        client_socket, client_adres = server_socket.accept()
        client_socket.setblocking(False)
        if len(pair_players) == 0:
            color = "w"
        else:
            color = "b"
        new_player = Player(client_socket, client_adres, color)
        print(f"{new_player.adres} connected")
        new_player.socket.send((new_player.color).encode('utf-8'))
        pair_players.append(new_player)
    except BlockingIOError:
        pass

    if len(pair_players) == 2:
        new_game = Game(pair_players[0], pair_players[1], game_id)
        games.append(new_game)
        game_id += 1
        for player in pair_players:
            player.socket.send(new_game.get_starts_parameters().encode('utf-8'))
        pair_players.clear()

    for game in games:
        if game.delay > 9:
            # do game
            pass
        else:
            game.delay += 1
    sleep(0.5)

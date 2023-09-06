from random import randint
from Player import Player
from Board import Board


class Game:
    id: int
    white_player: Player
    black_player: Player
    board: Board

    delay: int
    first: int

    def __init__(self,
                 white_player: Player,
                 black_player: Player,
                 id: int
                 ) -> None:
        self.white_player = white_player
        self.black_player = black_player
        self.id = id

        self.board = Board()
        self.delay = 0
        self.first = randint(0, 1)

    def start(self) -> None:
        self.board.show_board_in_console(rotate180=False)

    def get_starts_parameters(self) -> str:
        return "some"

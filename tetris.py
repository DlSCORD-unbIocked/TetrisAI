import numpy as np
import time
from board import Board


def main(genomes=None, config=None):
    # end will create 50 boards
    board_list = []
    board = Board(10, 20)
    while not board.game_over:
        key = input("\n> press key WASD to move the piece\n")

        board.update(key)

        # from StackOverflow for displaying
        print(
            "\n".join(["  ".join([str(cell) for cell in row]) for row in board.board])
        )


if __name__ == "__main__":
    main()

import numpy as np
import time
from board import Board


def main():
    # end will create 50 boards
    board_list = []
    board = Board(10, 20, None, None)
    print("\n".join(["  ".join([str(cell) for cell in row]) for row in board.board]))
    while not board.game_over:
        key = input("Enter a key: ")
        board.update(key)
        print(
            "\n".join(["  ".join([str(cell) for cell in row]) for row in board.board])
        )


if __name__ == "__main__":
    main()

import numpy as np
import time
from board import Board
import graphics, pygame


def main():
    # end will create 50 boards
    board = Board(10, 20, None, None)
    g = graphics.Graphics()
    while not board.game_over:
        g.draw_board(board)
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


if __name__ == "__main__":
    main()

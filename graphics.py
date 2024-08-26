import pygame
import numpy as np
from board import Board
import time


class Graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode((500, 1000))

    def draw_grid(self):
        for x in range(10):
            pygame.draw.line(self.screen, (255, 255, 255), (x * 50, 0), (x * 50, 1000))
            for y in range(20):

                pygame.draw.line(
                    self.screen, (255, 255, 255), (0, y * 50), (500, y * 50)
                )

    def draw_board(self, board):
        self.screen.fill((0, 0, 0))
        self.draw_grid()

        for (y, x), element in np.ndenumerate(board.get_board()):
            if element > 0:
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255),
                    (x * 50, y * 50, 50, 50),
                )

    def run(self, board):
        FPS = 30

        clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((500, 1000))
        t = time.time()
        while True:
            self.draw_board(board)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        board.update("a")
                    if event.key == pygame.K_d:
                        board.update("d")
                    if event.key == pygame.K_w:
                        board.update("w")
                    if event.key == pygame.K_SPACE:
                        board.update(" ")

            # board.update("s")
            if time.time() - t > 0.5:
                board.update("s")
                t = time.time()
            clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    b = Board(10, 20)
    g = Graphics()
    g.run(b)

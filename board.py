import numpy as np
from shapes import TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece
import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype=int)
        self.score = 0
        self.lines = 0
        self.level = 1
        self.piece = None
        self.game_over = False
        self.new_piece()

    def new_piece(self):
        print("new piece!")
        self.piece = random.choice(
            [TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece]
        )()

    def check_clear_lines(self):
        filled_rows = np.all(self.board, axis=1)
        if np.any(filled_rows):
            self.clear_lines(np.where(filled_rows)[0])

    def clear_lines(self, lines):
        self.board = np.delete(self.board, lines, axis=0)
        for _ in lines:
            self.board = np.insert(self.board, 0, 0, axis=0)
        self.score += len(lines)
        self.lines += len(lines)
        self.level = self.lines // 10 + 1

    def check_game_over(self):
        if np.any(self.board[0]):
            self.game_over = True

    def update(self, action=None):
        if action:

            for (x, y), element in np.ndenumerate(self.piece.get_blocks()):
                if element:
                    self.board[self.piece.get_x() + x, self.piece.get_y() + y] = 0

            if action == "w":
                self.piece.rotate()
            elif action == "a":
                self.piece.set_y(self.piece.get_y() - 1)
            elif action == "s":
                self.piece.set_x(self.piece.get_x() + 1)
            elif action == "d":
                self.piece.set_y(self.piece.get_y() + 1)
            elif action == " ":
                while not self.piece.check_collision():
                    self.piece.set_y(self.piece.get_y() + 1)

            if self.piece.check_collision(self.board):
                for (x, y), element in np.ndenumerate(self.piece.get_blocks()):
                    if element:
                        self.board[self.piece.get_x() + x, self.piece.get_y() + y] = 1
                self.check_clear_lines()
                del self.piece
                self.new_piece()
                return
            else:
                for (x, y), element in np.ndenumerate(self.piece.get_blocks()):
                    if element:
                        self.board[self.piece.get_x() + x, self.piece.get_y() + y] = 1
        if self.game_over:
            return

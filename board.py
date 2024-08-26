import numpy as np
from shapes import TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece
import random


class Board:
    def __init__(self, width, height, genome, net):
        self.width = width
        self.height = height
        self.genome = genome
        self.net = net
        self.board = np.zeros((height, width), dtype=int)
        self.score = 0
        self.lines = 0
        self.level = 1
        self.piece = TPiece()
        self.game_over = False
        self.next_piece = random.choice(
            [TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece]
        )()
        self.new_piece()

    def new_piece(self):
        print("new piece!")
        self.piece = self.next_piece
        self.next_piece = random.choice(
            [TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece]
        )()
        self.put_active()

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

    def clear_active(self):
        for (x, y), element in np.ndenumerate(self.piece.get_blocks()):
            if element:
                self.board[self.piece.get_x() + x, self.piece.get_y() + y] = 0

    def put_active(self):
        for (x, y), element in np.ndenumerate(self.piece.get_blocks()):
            if element:
                self.board[self.piece.get_x() + x, self.piece.get_y() + y] = 1

    def get_board(self):
        return self.board

    def update(self, action=None):
        if action:

            self.clear_active()

            if action == "w":
                self.piece.rotate()
            elif action == "a":
                self.piece.set_y(self.piece.get_y() - 1)
            # elif action == "s":
            #     self.piece.set_x(self.piece.get_x() + 1)
            elif action == "d":
                self.piece.set_y(self.piece.get_y() + 1)
            elif action == " ":
                while not self.piece.check_collision(self.board):
                    self.piece.set_x(self.piece.get_x() + 1)
                    self.clear_active()

            if self.piece.check_collision(self.board):
                self.put_active()
                self.check_clear_lines()
                del self.piece
                self.new_piece()
                return
            else:
                self.put_active()
        if self.game_over:
            return

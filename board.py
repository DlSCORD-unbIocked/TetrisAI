import numpy as np
from shapes import TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece
import random


class Board:
    def __init__(self, width, height, genome=None, net=None):
        self.width = width
        self.height = height
        self.genome = genome
        self.net = net
        self.board = np.zeros((height, width), dtype=int)
        self.piece_level = 0
        self.piece = TPiece()
        self.score = 0
        self.game_over = False
        self.rigid_std = 0
        self.next_piece = random.choice(
            [TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece]
        )()
        self.new_piece()

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = random.choice(
            [TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece]
        )()
        self.put_active()

    def check_clear_lines(self):
        filled_rows = np.all(self.board, axis=1)
        if np.any(filled_rows):
            self.clear_lines(np.where(filled_rows)[0])
        # return amount cleared
        return len(np.where(filled_rows)[0])

    def clear_lines(self, lines):
        self.board = np.delete(self.board, lines, axis=0)
        for _ in lines:
            self.board = np.insert(self.board, 0, 0, axis=0)
        lin = len(lines)
        self.score += 10 * (lin**2 - 10 + 1)

    def get_score(self):
        return self.score

    def set_piece_height(self):
        mask = np.any(self.board, axis=1)
        old = self.piece_level
        self.piece_level = 20 - np.where(mask)[0].min()
        rigid_diff = self.set_rigid_std()
        self.score += (old - self.piece_level) * 10 + rigid_diff * 10
        # detect hole
        if self.piece.check_collision(
            self.board,
            0,
        ):
            self.score -= 10
        else:
            self.score += 3

    def set_rigid_std(self):

        old = self.rigid_std
        self.rigid_std = np.std(np.sum(self.board, axis=0))
        return old - np.std(np.sum(self.board, axis=0))

    def check_game_over(self):
        if self.piece_level >= 19:
            self.score -= 30
            return True
        return False

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
                # had rotation errors going to other side of screen, so I added this
                if self.piece.check_side(self.board, -1):
                    self.piece.set_y(self.piece.get_y() + 2)
                    self.piece.rotate()
                    while not self.piece.check_side(self.board, -1):
                        self.piece.set_y(self.piece.get_y() - 1)

                elif self.piece.check_side(self.board, 1):
                    self.piece.set_y(self.piece.get_y() - 2)
                    self.piece.rotate()
                    while not self.piece.check_side(self.board, 1):
                        self.piece.set_y(self.piece.get_y() + 1)

                else:
                    self.piece.rotate()
            elif action == "a":
                if not self.piece.check_side(self.board, -1):
                    self.piece.set_y(self.piece.get_y() - 1)
            elif action == "s":
                if not self.piece.check_collision(self.board):
                    self.piece.set_x(self.piece.get_x() + 1)
            elif action == "d":
                if not self.piece.check_side(self.board, 1):
                    self.piece.set_y(self.piece.get_y() + 1)
            elif action == " ":
                while not self.piece.check_collision(self.board):
                    self.piece.set_x(self.piece.get_x() + 1)
                    self.clear_active()

            if self.piece.check_collision(self.board):
                self.put_active()
                self.check_clear_lines()
                self.set_piece_height()
                del self.piece
                self.new_piece()

            else:
                self.put_active()
        # when running AI
        self.genome.fitness = self.score
        if self.check_game_over():
            return False
        return True

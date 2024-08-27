import numpy as np
import random
from shapes import TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece


class Board:
    def __init__(self, width, height, genome=None, net=None):
        self.width = width
        self.height = height
        self.genome = genome
        self.net = net
        self.board = np.zeros((height, width), dtype=int)
        self.piece_level = 0
        self.score = 3
        self.game_over = False
        self.rigid_std = 0
        self.next_piece = random.choice([TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece])()
        self.new_piece()

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = random.choice([TPiece, SquarePiece, LinePiece, LeftLPiece, RightLPiece, LeftZPiece])()
        self.put_active()

    def check_clear_lines(self):
        filled_rows = np.all(self.board, axis=1)
        if np.any(filled_rows):
            self.clear_lines(np.where(filled_rows)[0])
        return len(np.where(filled_rows)[0])

    def clear_lines(self, lines):
        self.board = np.delete(self.board, lines, axis=0)
        for _ in lines:
            self.board = np.insert(self.board, 0, 0, axis=0)
        self.score += [800, 2400, 4800, 10000][len(lines) - 1]

    def get_score(self):
        return self.score

    def set_piece_height(self):
        mask = np.any(self.board, axis=1)
        old = self.piece_level
        self.piece_level = 20 - np.where(mask)[0].min()
        rigid_diff = self.set_rigid_std()
        self.score += (old - self.piece_level) * 20 + rigid_diff * 10
        self.score += 5 if not self.piece.check_collision(self.board, 0) else -20
        self.penalize_holes()
        #self.score -= self.calculate_stack_height() * 20
        self.score -= self.calculate_stack_unevenness()
        self.score += self.calculate_side_bonus()

    def calculate_side_bonus(self):
        side_columns = self.board[:, [0, 1, -2, -1]]
        return np.sum(side_columns) * 5

    def calculate_stack_unevenness(self):
        column_heights = self.height - np.where(self.board.any(axis=0))[0]
        return np.std(column_heights) * 30

    def set_rigid_std(self):
        old = self.rigid_std
        self.rigid_std = np.std(np.sum(self.board, axis=0))
        return old - self.rigid_std

    def check_game_over(self):
        if self.piece_level >= 19:
            self.score -= 10000
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

    def rotate_piece(self):
        original_position = (self.piece.get_x(), self.piece.get_y())
        original_rotation = self.piece.rotation
        self.piece.rotate()
        if not self.is_valid_position():
            for x_offset, y_offset in [(0, -1), (0, 1), (0, -2), (0, 2), (-1, 0), (1, 0)]:
                self.piece.set_x(original_position[0] + x_offset)
                self.piece.set_y(original_position[1] + y_offset)
                if self.is_valid_position():
                    return True
            self.piece.set_x(original_position[0])
            self.piece.set_y(original_position[1])
            self.piece.rotation = original_rotation
            for _ in range(3):
                self.piece.rotate()
            return False
        return True

    def is_valid_position(self):
        for x, y in self.piece.get_piece_coordinates():
            if x < 0 or x >= self.height or y < 0 or y >= self.width or self.board[x][y]:
                return False
        return True

    def calculate_holes(self):
        holes = 0
        for col in range(self.width):
            column = self.board[:, col]
            first_block = np.argmax(column > 0)
            if first_block > 0:
                hole_depths = np.arange(len(column[first_block:]))
                holes += np.sum(column[first_block:] == 0 * (hole_depths + 1))
        return holes

    def penalize_holes(self):
        self.score -= self.calculate_holes() * 15

    def calculate_stack_height(self):
        mask = np.any(self.board, axis=1)
        return self.height - np.where(mask)[0].min() if np.any(mask) else 0

    def update(self, action):
        try:
            if action:
                self.clear_active()
                if action == "w":
                    self.rotate_piece()
                elif action == "a" and not self.piece.check_side(self.board, -1):
                    self.piece.set_y(self.piece.get_y() - 1)
                elif action == "s" and not self.piece.check_collision(self.board):
                    self.piece.set_x(self.piece.get_x() + 1)
                elif action == "d" and not self.piece.check_side(self.board, 1):
                    self.piece.set_y(self.piece.get_y() + 1)
                elif action == " ":
                    while not self.piece.check_collision(self.board):
                        self.piece.set_x(self.piece.get_x() + 1)
                        self.clear_active()
                if self.piece.check_collision(self.board):
                    self.put_active()
                    self.check_clear_lines()
                    self.set_piece_height()
                    self.new_piece()
                else:
                    self.put_active()
            self.genome.fitness = self.score
            return not self.check_game_over()
        except IndexError:
            return False

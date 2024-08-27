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
        self.score = 3
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
        self.score += (old - self.piece_level) * 10 + rigid_diff * 5
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
            try:
                if element:
                    self.board[self.piece.get_x() + x, self.piece.get_y() + y] = 1
            except IndexError:
                self.piece.check_collision(self.board)

    def get_board(self):
        return self.board

    # AI GEN
    def rotate_piece(self):
        original_position = (self.piece.get_x(), self.piece.get_y())
        original_rotation = self.piece.rotation

        # Try to rotate
        self.piece.rotate()

        # Check if the rotation is valid
        if not self.is_valid_position():
            # If not valid, try wall kicks
            kick_offsets = [(0, -1), (0, 1), (0, -2), (0, 2), (-1, 0), (1, 0)]
            for x_offset, y_offset in kick_offsets:
                self.piece.set_x(original_position[0] + x_offset)
                self.piece.set_y(original_position[1] + y_offset)
                if self.is_valid_position():
                    return True  # Successful rotation with wall kick

            # If all wall kicks fail, revert the rotation
            self.piece.set_x(original_position[0])
            self.piece.set_y(original_position[1])
            self.piece.rotation = original_rotation
            for _ in range(3):  # Rotate back to original position
                self.piece.rotate()
            return False  # Rotation failed

        return True  # Rotation succeeded without wall kick

    def is_valid_position(self):
        for x, y in self.piece.get_piece_coordinates():
            if (
                x < 0
                or x >= self.height
                or y < 0
                or y >= self.width
                or self.board[x][y]
            ):
                return False
        return True

    def update(self, action):
        try:
            if action:

                self.clear_active()

                if action == "w":
                    self.rotate_piece()
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
        except IndexError:
            print("dooooooh")
            return False

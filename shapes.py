# created using AI
import numpy as np


class Shape:
    def __init__(self):
        self.blocks = np.array([])
        self.color = (255, 255, 255)
        self.x = 0
        self.y = 3
        self.id = 0
        self.rotation = 0

    def rotate(self):
        self.blocks = np.rot90(self.blocks, k=-1)
        if self.rotation == 3:
            self.rotation = 0
        else:
            self.rotation += 1

    def get_blocks(self):
        return self.blocks

    def get_color(self):
        return self.color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def check_collision(self, board, value=1):
        # using ndenumerate

        for (x, y), element in np.ndenumerate(self.blocks):
            board_x = self.x + x + 1
            board_y = self.y + y

            if element:
                try:
                    if value == 1 and (
                        board_x >= 20 or board[board_x, board_y] == value
                    ):
                        return True

                    if value == 0 and board[board_x, board_y] == value:
                        return True
                except IndexError:
                    pass

        return False

    def check_side(
        self,
        board,
        direction=1,
    ):

        for (x, y), element in np.ndenumerate(self.blocks):
            board_x = self.x + x
            board_y = self.y + y
            try:
                if element and (
                    self.y + y + direction < 0
                    or self.y + y + direction >= 10
                    or board[board_x, board_y] != 0
                ):
                    return True
            except IndexError:
                return True
        return False


# fmt: off


class TPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 255, 255)
        self.id = 1
        self.blocks = np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ])


class SquarePiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.y = 3
        self.id = 2
        self.color = (255, 255, 0)
        self.blocks = np.array([
            [1, 1],
            [1, 1]
        ])

    def rotate(self):
        pass


class LinePiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 255, 0)
        self.id = 3
        self.blocks = np.array([
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ])


class LeftLPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 0, 255)
        self.id = 4
        self.blocks = np.array([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ])


class RightLPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (255, 0, 0)
        self.id = 5
        self.blocks = np.array([
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ])


class LeftZPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 255, 0)
        self.id = 6
        self.blocks = np.array([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ])


class RightZPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (255, 0, 255)
        self.id = 7
        self.blocks = np.array([
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ])

if __name__ == "__main__":
    piece = LinePiece()
    for row in piece.get_blocks():
        print(row)
    piece.rotate()
    for row in piece.get_blocks():
        print(row)
    piece.rotate()
    for row in piece.get_blocks():
        print(row)

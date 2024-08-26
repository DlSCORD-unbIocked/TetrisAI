# fmt: off
# created using AI
class Shape:
    def __init__(self):
        self.blocks = []
        self.color = (255, 255, 255)
        self.x = 3
        self.y = 0

    def rotate(self):
        self.blocks = list(zip(*self.blocks[::-1]))

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

    def check_collision(self, board, x, y):
        pass


class TPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 255, 255)
        self.blocks = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]


class SquarePiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (255, 255, 0)
        self.blocks = [
            [1, 1],
            [1, 1]
        ]

    def rotate(self):
        pass


class LinePiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 255, 0)
        self.blocks = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]


class LeftLPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 0, 255)
        self.blocks = [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]


class RightLPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (255, 0, 0)
        self.blocks = [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ]


class LeftZPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (0, 255, 0)
        self.blocks = [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ]


class RightZPiece(Shape):
    def __init__(self):
        Shape.__init__(self)
        self.color = (255, 0, 255)
        self.blocks = [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ]

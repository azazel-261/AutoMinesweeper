class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y

    def to_list(self):
        return [self.x, self.y]

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()

class Cell:
    def __init__(self):
        self.marked = False
        self.opened = False
        self.number = 0

        self.screen_coords = Vector2(0, 0)

    def mark(self):
        self.marked = True

class Field:
    def __init__(self):
        self.width = 0
        self.height = 0

        self.cells: list[list[Cell]] = []

    @classmethod
    def count_open(cls, cells: list[Cell]) -> int:
        opened = 0
        for cell in cells:
            if cell.opened:
                opened += 1
        return opened

    @classmethod
    def count_marked(cls, cells: list[Cell]) -> int:
        marked = 0
        for cell in cells:
            if cell.marked:
                marked += 1
        return marked

    def init_empty(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]

    def get_cell(self, coords: Vector2) -> Cell | None:
        try: return self.cells[coords.y][coords.x]
        except IndexError: return None

    def get_adjacent(self, coords: Vector2) -> list[Vector2]:
        possible_x_diff = [-1, 0, 1]
        possible_y_diff = [-1, 0, 1]
        cells = []
        for x_diff in possible_x_diff:
            for y_diff in possible_y_diff:
                tmp_coords = Vector2(coords.x + x_diff, coords.y + y_diff)
                if tmp_coords.x < 0 or tmp_coords.y < 0:
                    continue
                if tmp_coords != coords and self.get_cell(tmp_coords) is not None:
                    cells.append(tmp_coords)
        return cells



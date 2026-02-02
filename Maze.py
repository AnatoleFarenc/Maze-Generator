from typing import Literal
from Cell import Cell


class Maze():
    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int]) -> None:
        self.__height = 0
        self.__width = 0
        self.__start: tuple[Literal[0], Literal[0]] = (0, 0)
        self.__end: tuple[Literal[0], Literal[0]] = (0, 0)
        self.height = height
        self.width = width
        self.start = start
        self.end = end
        self.grid = [[Cell(x, y, self.width, self.height)
                     for x in range(self.width)]
                     for y in range(self.height)]
        self.__mid_pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

    @property
    def start(self) -> tuple[int, int]:
        return self.__start

    @property
    def end(self) -> tuple[int, int]:
        return self.__end

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @start.setter
    def start(self, start: tuple) -> None:
        x, y = start
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.__start = start

    @end.setter
    def end(self, end: tuple) -> None:
        if end[0] >= 0 and end[0] < self.width:
            if end[1] >= 0 and end[1] < self.height:
                self.__end = end

    @height.setter
    def height(self, height: int):
        if height > 0:
            self.__height = height

    @width.setter
    def width(self, width: int) -> None:
        if width > 0:
            self.__width = width

    def __getitem__(self, index: int):
        if not (0 <= index < self.height):
            raise IndexError(f"Error: index {index} out of range "
                             f"({self.width}, {self.height})")
        return self.grid[index]

    def add_connection(self, cell_1: tuple, cell_2: tuple) -> None:
        """ Adds a connection between two cells in the maze by removing the
            wall separating them """
        x1, y1 = cell_1
        x2, y2 = cell_2
        cell_value1 = self[y1][x1]
        cell_value2 = self[y2][x2]
        if x1 < x2:
            cell_value1.remove_wall("East")
            cell_value2.remove_wall("West")
        elif x1 > x2:
            cell_value1.remove_wall("West")
            cell_value2.remove_wall("East")
        elif y1 < y2:
            cell_value1.remove_wall("South")
            cell_value2.remove_wall("North")
        elif y1 > y2:
            cell_value1.remove_wall("North")
            cell_value2.remove_wall("South")
        else:
            raise ValueError("Error adding connection: Invalid cell values:"
                             f"cell_1={cell_1}, cell_2={cell_2}")

    def upscacle_pattern(self) -> list:
        if self.height < 7 or self.width < 9:
            return None

        if self.height <= 15 or self.width <= 21:
            return self.__mid_pattern

        width_pattern = self.width * (2/3)
        height_pattern = self.height * (2/3)
        width_scale = max(1, int(width_pattern / len(self.__mid_pattern)))
        height_scale = max(1, int(height_pattern / len(self.__mid_pattern[0])))
        scale = min(height_scale, width_scale)

        new_pattern = []

        # upsaclse patternd
        for line in self.__mid_pattern:
            scale_line = []
            for value in line:
                scale_line.extend([value] * scale)
            for _ in range(scale):
                new_pattern.append(scale_line.copy())

        return new_pattern

    def append_patern(self) -> None:
        self.__mid_pattern = self.upscacle_pattern()
        if not self.__mid_pattern:
            return
        height = self.height
        width = self.width
        pattern_h = len(self.__mid_pattern)
        pattern_w = len(self.__mid_pattern[0])
        s_row = (height - pattern_h) // 2
        s_col = (width - pattern_w) // 2

        for i in range(pattern_h):
            for j in range(pattern_w):
                if (0 <= s_row + i < height and 0 <= s_col + j < width):
                    if self.__mid_pattern[i][j] == 1:
                        self.grid[s_row + i][s_col + j].visited = True
                        self.grid[s_row + i][s_col + j].full = True

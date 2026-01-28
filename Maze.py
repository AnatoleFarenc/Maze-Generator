from Cell import Cell


class Maze():
    def __init__(self, width: int, height: int, start: tuple,
                 end: tuple) -> None:
        self.__height = 0
        self.__width = 0
        self.__start = (0, 0)
        self.__end = (0, 0)
        self.height = height
        self.width = width
        self.start = start
        self.end = end
        self.grid = [[Cell(x, y, self.width, self.height)
                     for x in range(self.width)]
                     for y in range(self.height)]

    @property
    def start(self) -> tuple:
        return self.__start

    @property
    def end(self) -> tuple:
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

    def debug_grid(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                print(self.grid[y][x].get_hex_value(), end=" ")
            print()

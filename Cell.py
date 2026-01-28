class Cell():
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.__x = 0
        self.__y = 0
        self.__height = 0
        self.__width = 0
        self.__color = 0
        self.__wall_bits = 0b1111
        self.__visited = False

        self.x = x
        self.y = y
        self.height = height
        self.width = width

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def cordinate(self) -> tuple:
        return (self.x, self.y)

    @property
    def visited(self) -> bool:
        return self.__visited

    @x.setter
    def x(self, x: int) -> None:
        if x >= 0:
            self.__x = x
        else:
            raise ValueError(f"Error: Value (x:{x}) outside of grid")

    @y.setter
    def y(self, y: int) -> None:
        if y >= 0:
            self.__y = y
        else:
            raise ValueError(f"Error: Value (y:{y}) outside of grid")

    @height.setter
    def height(self, height: int) -> None:
        if height > 0:
            self.__height = height

    @width.setter
    def width(self, width: int) -> None:
        if width > 0:
            self.__width = width

    @cordinate.setter
    def cordinate(self, cordinate: tuple) -> None:
        self.x = cordinate[0]
        self.y = cordinate[1]

    @visited.setter
    def visited(self, is_visited: bool) -> None:
        self.__visited = is_visited

    def get_value(self) -> int:
        return int(self.__wall_bits)

    def get_hex_value(self):
        return f"{hex(self.__wall_bits).removeprefix('0x').upper()}"

    def remove_wall(self, direction: str) -> None:
        """ Removes the cell's wall in the given direction """
        binary_value = self.__wall_bits
        direction = direction.lower().title()
        match direction:
            case "North":
                offset = 0
            case "East":
                offset = 1
            case "South":
                offset = 2
            case "West":
                offset = 3
            case _:
                raise ValueError("ERROR: Could not remove wall - invalid "
                                 f"direction '{direction}'")
        binary_value &= ~(1 << offset)
        self.__wall_bits = binary_value

    def get_walls(self) -> list:
        walls = []
        walls_value = 0b0000
        walls_value += self.get_value()
        if (walls_value >> 0) & 1:
            walls.append("North")
        if (walls_value >> 1) & 1:
            walls.append("East")
        if (walls_value >> 2) & 1:
            walls.append("South")
        if (walls_value >> 3) & 1:
            walls.append("West")
        return walls

from typing import Tuple
from math import inf


class Cell():
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.__x = 0
        self.__y = 0
        self.__height = 0
        self.__width = 0
        self.__wall_bits = 0b1111
        self.__visited = False
        self.__full = False
        # atribut for pathfinding
        self.__parent = None
        self.__cost = inf
        self.__g_h_cost = inf

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

    @property
    def full(self) -> bool:
        return self.__full

    @property
    def parent(self) -> Tuple[int, int]:
        return self.__parent

    @parent.setter
    def parent(self, parent) -> None:
        self.__parent = parent

    @property
    def cost(self) -> int:
        return self.__cost
    
    @cost.setter
    def cost(self, cost) -> None:
        self.__cost = cost

    @property
    def g_h_cost(self) -> int:
        return self.__g_h_cost

    @g_h_cost.setter
    def g_h_cost(self, g_h) -> None:
        self.__g_h_cost = g_h

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

    @full.setter
    def full(self, value: bool) -> None:
        self.__full = value

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
        """ Returns a binary value which indicates which walls are
            present around the cell """
        return int(self.__wall_bits)

    def get_hex_value(self):
        """ Returns a formatted version of the cell's wall value """
        return f"{hex(self.__wall_bits).removeprefix('0x').upper()}"

    def remove_wall(self, direction: str) -> None:
        """ Removes the cell's wall in the given direction by modifying
            its wall value """
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
        """ Returns a list of every existing wall around the cell """
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

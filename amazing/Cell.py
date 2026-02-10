from math import inf
from typing import Tuple, Union, Optional


class Cell():
    """ Represent one cell of maze """
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """ Initialize cordinate in maze and width, height of maze """
        self.__x = 0
        self.__y = 0
        self.__height = 0
        self.__width = 0
        self.__wall_bits = 0b1111
        self.__visited = False
        self.__full = False

        self.__parent: Optional[Tuple[int, int]] = None
        self.__cost = inf
        self.__g_h_cost = inf

        self.x = x
        self.y = y
        self.height = height
        self.width = width

    @property
    def x(self) -> int:
        """ Return x pos """
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        """ Set x pos """
        if x >= 0:
            self.__x = x
        else:
            raise ValueError(f"Error: Value (x:{x}) outside of grid")

    @property
    def y(self) -> int:
        """ Return y pos """
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        """ Set y pos """
        if y >= 0:
            self.__y = y
        else:
            raise ValueError(f"Error: Value (y:{y}) outside of grid")

    @property
    def height(self) -> int:
        """ Return height maze """
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        """ Set height parameter of maze """
        if height > 0:
            self.__height = height

    @property
    def width(self) -> int:
        """ Return width maze """
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        """ Set widht parameter of maze """
        if width > 0:
            self.__width = width

    @property
    def coordinates(self) -> tuple:
        """ Return (x, y) coordinate of cell """
        return (self.x, self.y)

    @coordinates.setter
    def coordinates(self, coordinates: tuple) -> None:
        """ Set cell Coordinates """
        self.x = coordinates[0]
        self.y = coordinates[1]

    @property
    def visited(self) -> bool:
        """ Return if cell is visited """
        return self.__visited

    @visited.setter
    def visited(self, is_visited: bool) -> None:
        """ Set cell visited or not """
        self.__visited = is_visited

    @property
    def full(self) -> bool:
        """ Return if cell is full or not """
        return self.__full

    @full.setter
    def full(self, value: bool) -> None:
        """ Set cell full or not """
        self.__full = value

    @property
    def parent(self) -> Optional[Tuple[int, int]]:
        """ Return coordinate of parent Cell. Used in maze pathinding"""
        return self.__parent

    @parent.setter
    def parent(self, parent: Optional[Tuple[int, int]]) -> None:
        """ Set coordinat of parent """
        self.__parent = parent

    @property
    def cost(self) -> Union[int, float]:
        """ Return the cost of this Cell.
        (the distance from start passing through parrents) """
        return self.__cost

    @cost.setter
    def cost(self, cost: int) -> None:
        """ Set cost of this cell """
        self.__cost = cost

    @property
    def g_h_cost(self) -> Union[int, float]:
        """
        Return the estimated cost:

        f(n) = g(n) + h(n)

        g(n) -> Cost of distance from start passint through parents

        h(n) -> Heuristic cost form cell cordinate to end cell without wall
        """
        return self.__g_h_cost

    @g_h_cost.setter
    def g_h_cost(self, g_h: int) -> None:
        """ Set estimated cost """
        self.__g_h_cost = g_h

    def get_value(self) -> int:
        """ Returns a binary value which indicates which walls are
            present around the cell """
        return int(self.__wall_bits)

    def get_hex_value(self) -> str:
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

    def get_walls(self) -> list[str]:
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

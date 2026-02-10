"""
Maze generation reusable module.

This module provides all the required classes to generate, manipulate,
and solve a maze. It is designed to be reusable and importable in
future projects.

Main class:
    MazeGenerator

The maze generation logic is encapsulated inside the MazeGenerator class,
which operates on a Maze object and produces a fully generated maze.
The internal maze representation is independent from any output file
format.

------------------------------------------------------------
Basic usage example
------------------------------------------------------------

    from mazegen import Maze, MazeGenerator, Pathfinder

    maze = Maze(width=10, height=10, start=(0, 0), end=(9, 9))
    generator = MazeGenerator(maze)
    generator.seed = 42
    generator.generate()

    generated_maze = generator.maze

    pathfinder = Pathfinder(generated_maze)
    solution = pathfinder.get_directions()

------------------------------------------------------------
Example using a configuration dictionary
------------------------------------------------------------

    config = {
        "WIDTH": 10,
        "HEIGHT": 10,
        "ENTRY": (0, 0),
        "EXIT": (9, 9),
        "PERFECT": True,
        "SEED": 42,
        "OUTPUT_FILE": "maze.txt"
    }

    generator = MazeGenerator.create_instance(config)
    maze = generator.maze

------------------------------------------------------------
Accessing generated data
------------------------------------------------------------

Maze structure:
    - maze.grid           : 2D list of Cell objects
    - maze[y][x]          : Access a specific Cell
    - cell.get_walls()    : Get walls around a cell

Maze solution:
    - Pathfinder.find_exit(start_cell) : Returns the solution path as a list
      of Cell objects
    - Pathfinder.get_directions()      : Returns the solution as directions
      (N, S, E, W)
    - Pathfinder.get_direction_string(): Returns the solution as a string

------------------------------------------------------------
Notes
------------------------------------------------------------

- The maze generator supports perfect and imperfect mazes.
- Random generation can be controlled using a seed.
- The solution path is guaranteed to exist between ENTRY and EXIT.
"""

import sys
import random
from typing import (Union, Optional, TypeVar, Type,
                    Tuple, List, Iterator, Dict, Any)
from math import inf
import time

T_GENERATE = TypeVar("T_GENERATE", bound="MazeGenerator")


def is_valid_config(config: Dict) -> None:
    """ Checks that the config data contains all the mandatory keys, and that
        their values are correct. Raises a ValueError if any errors are
        detected """
    mandatory_keys = {"WIDTH", "HEIGHT", "ENTRY",
                      "EXIT", "OUTPUT_FILE", "PERFECT",
                      "SEED", "WALLS", "OBJECTIVES", "PATH"}
    # Checks that all the mandatory keys are in the dictionary
    for key in mandatory_keys:
        if key not in config:
            raise ValueError(f"Error parsing config file - Missing '{key}' "
                             "key")
    # Checks that the height and width values are integers
    for key in ("WIDTH", "HEIGHT"):
        if not isinstance(config[key], int):
            raise ValueError(f"Error parsing config file - '{config[key]}' is "
                             f"not a valid input for {key} (must be int)")
    # Checks that the maze means the minimum size requirements
    if config["WIDTH"] * config["HEIGHT"] < 4:
        raise ValueError("Error parsing config file - Maze of size "
                         f"{config['WIDTH']}x{config['HEIGHT']} is too small "
                         "(2x2 minimum)")
    # Checks that the Entry and Exit tuples contain exactly two integers
    for key in ("ENTRY", "EXIT"):
        if len(config[key]) != 2:
            raise ValueError(f"Error parsing config file - {key} must have "
                             f"exactly 2 values: {config[key]} is invalid")
        x, y = config[key]
        if x >= config["WIDTH"] or y >= config["HEIGHT"]:
            raise ValueError(f"Error parsing config file - {key} coordinates "
                             f"{config[key]} outside of range "
                             f"({config['WIDTH']-1},{config['HEIGHT']-1})")
        elif x < 0 or y < 0:
            raise ValueError(f"Error parsing config file - {key} coordinates "
                             f"{config[key]} must be positive")
    # Checks that the Entry and Exit are not on the same cell
    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("Error parsing config file - Entry and Exit cannot "
                         "occupy the same cell")
    # Checks that the config file is a plain text file (.txt)
    if not isinstance(config["OUTPUT_FILE"], str):
        raise ValueError("Error parsing config file - Invalid output_file "
                         f"name '{config['OUTPUT_FILE']}'")
    if not config["OUTPUT_FILE"].endswith(".txt"):
        raise ValueError("Error parsing config file - Invalid "
                         f"output_file extension '{config['OUTPUT_FILE']}'"
                         " (extension must be '.txt')")
    # Checks that the perfect value is a boolean
    if not isinstance(config["PERFECT"], bool):
        raise ValueError("Error parsing config file - Invalid 'Perfect' "
                         "key value\nMust be 'True' or 'False'")
    # Checks that the Seed value is an int
    if not isinstance(config["SEED"], int):
        raise ValueError(f"Error parsing config file - '{config['SEED']}' is "
                         f"not a valid input for 'SEED' (must be int)")
    # Checks that the Walls value is a string
    if not isinstance(config["WALLS"], str):
        raise ValueError("Error parsing config file - Invalid 'WALLS' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Objectives value is a string
    if not isinstance(config["OBJECTIVES"], str):
        raise ValueError("Error parsing config file - Invalid 'OBJECTIVES' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Path value is a string
    if not isinstance(config["PATH"], str):
        raise ValueError("Error parsing config file - Invalid 'PATH' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Walls value is a valid color
    if config["WALLS"].upper() not in {"WHITE", "RED", "GREEN",
                                       "BLUE", "YELLOW", "PURPLE"}:
        raise ValueError("Error parsing config file - Invalid 'WALLS' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Objectives value is a valid color
    if config["OBJECTIVES"].upper() not in {"WHITE", "RED", "GREEN",
                                            "BLUE", "YELLOW", "PURPLE"}:
        raise ValueError("Error parsing config file - Invalid 'OBJECTIVES' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Path value is a valid color
    if config["PATH"].upper() not in {"WHITE", "RED", "GREEN",
                                      "BLUE", "YELLOW", "PURPLE"}:
        raise ValueError("Error parsing config file - Invalid 'PATH' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")


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


class Maze():
    """ Maze class """
    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int]) -> None:
        """ Init minimum setting of maze """
        self.height = height
        self.width = width
        self.start = start
        self.end = end
        self.grid: List[List[Cell]] = [
            [Cell(x, y, self.width, self.height)
             for x in range(self.width)]for y in range(self.height)]
        self.__mid_pattern = [[1, 0, 0, 0, 1, 1, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 1, 1, 0, 1, 1, 1],
                              [0, 0, 1, 0, 1, 0, 0],
                              [0, 0, 1, 0, 1, 1, 1]]

    @property
    def start(self) -> tuple[int, int]:
        """ Return start coordinate """
        return self.__start

    @start.setter
    def start(self, start: tuple) -> None:
        """ Set start coordinate """
        x, y = start
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.__start = start
        else:
            raise ValueError(f"Error: maze start out of range ({start})")

    @property
    def end(self) -> tuple[int, int]:
        """ Return end coordinate """
        return self.__end

    @end.setter
    def end(self, end: tuple) -> None:
        """ Set end coordinate """
        if end[0] >= 0 and end[0] < self.width:
            if end[1] >= 0 and end[1] < self.height:
                self.__end = end
                return
        raise ValueError(f"Error: maze end out of range ({end})")

    @property
    def height(self) -> int:
        """ Return height of maze """
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        """ Set height of maze """
        if height > 0:
            self.__height = height
        else:
            raise ValueError(f"Error: height to small: ({height})")

    @property
    def width(self) -> int:
        """ Return Width of maze """
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        """ Set width of maze """
        if width > 0:
            self.__width = width
        else:
            raise ValueError(f"Error: witdth to small: ({width})")

    @property
    def seed(self) -> int:
        return self.__seed

    @seed.setter
    def seed(self, seed: int) -> None:
        if not isinstance(seed, int):
            raise ValueError(f"Error: Invalid seed: ({seed})")
        self.__seed = seed

    def __getitem__(self, index: int) -> list[Cell]:
        """ Return cell of maze grid """
        if not (0 <= index < self.height):
            raise IndexError(f"Error: index {index} out of range "
                             f"({self.width}, {self.height})")
        return self.grid[index]

    def __iter__(self) -> Iterator[list[Cell]]:
        """ Create an iterator for maze grid """
        return iter(self.grid)

    def get_hex_data(self) -> str:
        """ Return wall value of cell in hex format """
        output_data = ""
        for row in self:
            for cell in row:
                output_data += cell.get_hex_value()
            output_data += '\n'

        return output_data

    def get_cell(self, coordinate: Tuple[int, int]) -> Cell:
        """ Return Cell in grid maze """
        x, y = coordinate
        if x < 0 and x > self.width:
            raise ValueError(f"Error finding cell - x coordinate {x} is "
                             "outside of the maze dimensions")
        if y < 0 and x > self.height:
            raise ValueError(f"Error finding cell - y coordinate {y} is "
                             "outside of the maze dimensions")

        return self[y][x]

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
                             f"cell_1 = {cell_1}, cell_2 = {cell_2}")

    def upscale_pattern(self) -> list:
        """ Upscale 42 pattern from the size of maze (1/3) """
        if self.height < 7 or self.width < 9:
            return []

        if self.height <= 15 or self.width <= 21:
            return self.__mid_pattern

        width_pattern = self.width * (2 / 3)
        height_pattern = self.height * (2 / 3)
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

    def append_pattern(self) -> None:
        """ Add a scalable 42 pattern in the middle of maze grid """
        self.__mid_pattern = self.upscale_pattern()
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
                        self[s_row + i][s_col + j].visited = True
                        self[s_row + i][s_col + j].full = True

        x, y = self.start
        while self[y][x].full:
            y -= 1
            self.start = (x, y)
        x, y = self.end
        while self[y][x].full:
            y += 1
            self.end = (x, y)
        if self.start == self.end:
            raise ValueError("Entry or exit generated inside the 42 pattern. "
                             "Failed to resolve issue. Please try again with "
                             "different entry/exit values.")


class MazeGenerator():
    """ Create path in grid of maze to create a real maze """
    def __init__(self, maze: Maze) -> None:
        """ Create default variable and set recursion limit """
        sys.setrecursionlimit(10_000)
        self.__maze: Maze = maze
        self.stack = []
        self.seed = time.time_ns()
        self.maze.seed = self.seed

    @property
    def maze(self) -> Maze:
        """ Return Maze """
        if self.__maze is None:
            raise ValueError("Error creating maze - Maze has not been "
                             "initialized")
        return self.__maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        """ Set maze attribute with Maze """
        self.__maze = maze

    @property
    def seed(self) -> Union[int, None]:
        """ Retrun seed to random generation """
        return self.__seed

    @seed.setter
    def seed(self, seed: Union[int, None]) -> None:
        """ Set seed and create random generator """
        self.__seed = seed
        if seed:
            self.maze.seed = seed
        self.__rng = random.Random(self.seed)

    @property
    def stack(self) -> list[Cell]:
        """ Return stack """
        return self.__stack

    @stack.setter
    def stack(self, stack: list[Cell]) -> None:
        """ Create stack """
        self.__stack = stack

    @property
    def rng(self) -> random.Random:
        """ Return random value with generator """
        return self.__rng

    def check_coordinate_in_range(self, coordinate: tuple[int, int]) -> bool:
        """ Return if the coordianate isn't out the range of maze grid """
        x, y = coordinate
        if x < 0 or x >= self.maze.width:
            return False
        if y < 0 or y >= self.maze.height:
            return False
        return True

    def pop_stack(self) -> Cell:
        """ Return and remove first Cell on stack """
        cell: Cell = self.__stack.pop()
        return cell

    def push_stack(self, cell: Cell) -> None:
        """ Add Cell in end of stack """
        self.__stack.append(cell)

    def check_neighbours(self, current: Cell) -> Cell | None:
        """ Return a random valid neighbour cell """
        neighbours = []

        neighbour = {"top": (current.x, current.y - 1),
                     "right": (current.x + 1, current.y),
                     "bot": (current.x, current.y + 1),
                     "left": (current.x - 1, current.y)}

        for _, value in neighbour.items():
            if self.check_coordinate_in_range(value):
                if not self.maze[value[1]][value[0]].visited:
                    neighbours.append(self.maze[value[1]][value[0]])
        if len(neighbours) > 0:
            return self.rng.choice(neighbours)
        return None

    def create_paths(self, current: Cell) -> None:
        """ Create path in grid to generate maze """
        current.visited = True
        next = self.check_neighbours(current)
        if next:
            next.visited = True
            self.push_stack(current)
            self.maze.add_connection(current.coordinates, next.coordinates)
            self.create_paths(next)
        elif len(self.stack) > 0:
            self.create_paths(self.pop_stack())

    def can_break_wall(self, current: Cell, neighbor: Cell) -> bool:
        """ Checks if the wall between current and neighbor can be broken """
        def is_valid(coordinate: tuple) -> bool:
            c_x, c_y = coordinate
            if not self.check_coordinate_in_range((c_x, c_y)):
                return False
            cell = self.maze.get_cell((c_x, c_y))
            return cell == current or cell == neighbor or not cell.full

        x, y = current.coordinates
        offsets = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                   (x - 1, y), (x, y), (x + 1, y),
                   (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        cell_less_wall = 0
        for coordinate in offsets:
            if is_valid(coordinate):
                check_n = self.maze.get_cell(coordinate)
                if len(check_n.get_walls()) <= 2:
                    cell_less_wall += 1
        if cell_less_wall >= 8:
            return False
        return True

    def break_walls(self) -> None:
        """ Break random walls to create imperfect maze """
        h = self.maze.height
        w = self.maze.width
        r = (h * w)

        for _ in range(r):
            x = self.rng.randint(0, w - 1)
            y = self.rng.randint(0, h - 1)

            current = self.maze.get_cell((x, y))
            if current.full:
                continue
            neighbours = [(x, y - 1), (x + 1, y),
                          (x, y + 1), (x - 1, y)]
            neighbour_pos = self.rng.choice(neighbours)
            if not self.check_coordinate_in_range(neighbour_pos):
                continue
            neighbour = self.maze.get_cell(neighbour_pos)
            if neighbour.full:
                continue
            if self.can_break_wall(current, neighbour):
                self.maze.add_connection(current.coordinates, neighbour_pos)

    def generate(self) -> None:
        """ Generates a maze with the 42 pattern in the center """
        try:
            self.maze.append_pattern()
            x, y = self.maze.start
            self.create_paths(self.maze[y][x])
        except RecursionError:
            raise ValueError("The maze you tried to create is too large!\n"
                             "Please reduce its size and try again")

    @classmethod
    def create_instance(cls: Type[T_GENERATE], config: dict) -> T_GENERATE:
        """ Return MazeGenerator Object """
        height = config["HEIGHT"]
        width = config["WIDTH"]
        start = config["ENTRY"]
        end = config["EXIT"]
        perfect = config["PERFECT"]
        seed = config["SEED"]

        maze = Maze(width, height, start, end)
        generator = cls(maze)

        if seed != 0:
            generator.seed = seed

        generator.generate()

        if not perfect:
            generator.break_walls()

        return generator


class Pathfinder():
    """ Represent the more short path between two cell in maze """
    def __init__(self, maze: Maze):
        """ Init minimun setting of pathinder """
        self.__maze: Maze = maze
        self.__open: List[Cell] = []
        self.__close: List[Cell] = []
        self.start = self.maze.get_cell(maze.start)
        self.end = self.maze.get_cell(maze.end)

    @property
    def maze(self) -> Maze:
        """ Return maze """
        return self.__maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        """ Set maze """
        self.__maze = maze

    @property
    def open(self) -> List[Any]:
        """ Return open stack """
        return self.__open

    @property
    def close(self) -> List[Any]:
        """ Return close stack """
        return self.__close

    @property
    def start(self) -> Cell:
        """ Return start cell """
        return self.__start

    @start.setter
    def start(self, n_start: Cell) -> None:
        """ Set start cell """
        self.__start = n_start

    @property
    def end(self) -> Cell:
        """ Return end cell """
        return self.__end

    @end.setter
    def end(self, n_end: Cell) -> None:
        """ Set end cell """
        self.__end = n_end

    def get_neighbors(self, current: Cell) -> List[Cell]:
        """ Return list of neighbor without wall with current cell """
        neighborhood = []
        walls = current.get_walls()

        if not ("North" in walls):
            neighborhood.append(self.maze[current.y - 1][current.x])
        if not ("East" in walls):
            neighborhood.append(self.maze[current.y][current.x + 1])
        if not ("South" in walls):
            neighborhood.append(self.maze[current.y + 1][current.x])
        if not ("West" in walls):
            neighborhood.append(self.maze[current.y][current.x - 1])
        return neighborhood

    def get_heuristic_path(self, current: Cell) -> int:
        """ Return heurisitic path with by using Manhattan distance """
        x, y = current.coordinates
        x_end, y_end = self.maze.end

        # Manhattan distance
        return (int(abs(x - x_end) + abs(y - y_end)))

    def find_exit(self, start: Cell) -> List[Any]:
        """ Return Cell list of path to start at end """
        # Check if I've reached the end
        self.open.append(self.start)
        self.start.cost = 0
        self.start.parent = None
        self.start.g_h_cost = self.get_heuristic_path(self.start)

        while self.open:
            current = min(self.open, key=lambda cell: cell.g_h_cost)

            if current.coordinates == self.end.coordinates:
                path = []
                node = current
                while node:
                    path.append(node)
                    node = node.parent
                return path[::-1]

            # Append cell to the close list
            self.open.remove(current)
            self.close.append(current)

            # Find the greater cell for the next path
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                g_value = current.cost + 1
                h_value = self.get_heuristic_path(neighbor)

                if neighbor in self.close:
                    continue

                if neighbor not in self.open:
                    # cost calculation: f=g+h
                    neighbor.cost = g_value
                    neighbor.g_h_cost = g_value + h_value
                    neighbor.parent = current
                    self.open.append(neighbor)
                else:
                    if neighbor.cost > g_value:
                        neighbor.cost = g_value
                        neighbor.g_h_cost = g_value + h_value
                        neighbor.parent = current
        return []

    def get_directions(self) -> List[str]:
        """ Return direction list for describ the path """
        x, y = self.maze.start
        path_cell_list = self.find_exit(self.maze[y][x])

        directions = []
        for i in range(len(path_cell_list) - 1):
            cur_x, cur_y = path_cell_list[i].coordinates
            next_x, next_y = path_cell_list[i + 1].coordinates
            if cur_y > next_y:
                directions.append("N")
            elif cur_y < next_y:
                directions.append("S")
            elif cur_x < next_x:
                directions.append("E")
            elif cur_x > next_x:
                directions.append("W")

        return directions

    def get_direction_string(self) -> str:
        """ Return string of direction list"""
        direction_string = ""
        for dir in self.get_directions():
            direction_string += dir

        return direction_string


def create_new_maze(config: dict) -> Maze:
    """ Generates a new maze using the current configuration, and writes its
        data to the output file """
    try:
        is_valid_config(config)
    except ValueError as e:
        raise ValueError("Error creating maze - received invalid config:"
                         f"\n{e}")
    maze_gen = MazeGenerator.create_instance(config)

    return maze_gen.maze


def write_maze_to_file(config: dict, maze: Maze) -> None:
    """ Creates a file containing the maze data at the location designated
        in the config file by the OUTPUT_FILE key """
    output_file = config["OUTPUT_FILE"]
    start = config["ENTRY"]
    end = config["EXIT"]

    output_data = maze.get_hex_data()

    pathfinder = Pathfinder(maze)
    directions = pathfinder.get_direction_string()

    with open(output_file, "w") as fd:
        fd.write(output_data)
        fd.write('\n')
        fd.write(f"{start[0]},{start[1]}")
        fd.write('\n')
        fd.write(f"{end[0]},{end[1]}")
        fd.write('\n')
        fd.write(directions)


def test() -> None:
    def display_grid(maze: Maze) -> None:
        for i in range(maze.height):
            for j in range(maze.width):
                print(maze[i][j].get_hex_value(), end=" ")
            print()

    maze = Maze(10, 10, (0, 0), (9, 9))
    maze_gen = MazeGenerator(maze)
    maze_gen.generate()
    print("#### Perfect maze ###\n")
    display_grid(maze)

    print("\n### Imperfect maze ###\n")
    maze_gen.break_walls()
    display_grid(maze)


def test_with_cls() -> None:
    def display_grid(maze: Maze) -> None:
        for i in range(maze.height):
            for j in range(maze.width):
                print(maze[i][j].get_hex_value(), end=" ")
            print()
    config = {
        "HEIGHT": 10,
        "WIDTH": 10,
        "ENTRY": (0, 0),
        "EXIT": (9, 9),
        "PERFECT": True,
        "SEED": 10
    }
    maze_gen = MazeGenerator.create_instance(config)
    maze_gen.generate()

    print("#### Perfect maze ###\n")
    print(f"Config: {config}\n")
    display_grid(maze_gen.maze)

    print("\n### Imperfect maze ###\n")
    print(f"Config: {config}\n")
    config["PERFECT"] = False
    maze_gen = MazeGenerator.create_instance(config)
    maze_gen.generate
    display_grid(maze_gen.maze)


if __name__ == "__main__":
    print("Generate maze without config dict:\n")
    test()

    print("\n\n")
    print("Generate maze with config dict:\n")
    test_with_cls()

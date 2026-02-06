import sys
import random
from typing import Union, Optional, TypeVar, Type
from .Cell import Cell
from .Maze import Maze
from .parser import is_valid_config
from .file_handler import write_maze_to_file

T_GENERATE = TypeVar("T_GENERATE", bound="MazeGenerator")


class MazeGenerator():
    def __init__(self) -> None:
        sys.setrecursionlimit(10_000)
        self.__maze: Optional[Maze] = None
        self.stack = []
        self.seed = 0

    @property
    def maze(self) -> Maze:
        if self.__maze is None:
            raise ValueError("Error creating maze - Maze has not been "
                             "initialized")
        return self.__maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        self.__maze = maze

    @property
    def seed(self) -> Union[int, None]:
        return self.__seed

    @seed.setter
    def seed(self, seed: Union[int, None]) -> None:
        self.__seed = seed
        self.__rng = random.Random(self.seed)

    @property
    def stack(self) -> list[Cell]:
        return self.__stack

    @stack.setter
    def stack(self, stack: list[Cell]) -> None:
        self.__stack = stack

    @property
    def rng(self) -> random.Random:
        return self.__rng

    def check_cordinate_in_range(self, cordinate: tuple[int, int]) -> bool:
        x, y = cordinate
        if x < 0 or x >= self.maze.width:
            return False
        if y < 0 or y >= self.maze.height:
            return False
        return True

    def pop_stack(self) -> Cell:
        cell: Cell = self.__stack.pop()
        return cell

    def push_stack(self, cell: Cell) -> None:
        self.__stack.append(cell)

    def check_neighbours(self, current: Cell) -> Cell | None:
        neighbours = []

        neighbour = {"top": (current.x, current.y - 1),
                     "right": (current.x + 1, current.y),
                     "bot": (current.x, current.y + 1),
                     "left": (current.x - 1, current.y)}

        for _, value in neighbour.items():
            if self.check_cordinate_in_range(value):
                if not self.maze[value[1]][value[0]].visited:
                    neighbours.append(self.maze[value[1]][value[0]])
        if len(neighbours) > 0:
            return self.rng.choice(neighbours)
        return None

    def create_paths(self, current: Cell) -> None:
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
        def is_valid(cordinate: tuple) -> bool:
            c_x, c_y = cordinate
            if not self.check_cordinate_in_range((c_x, c_y)):
                return False
            cell = self.maze.get_cell((c_x, c_y))
            return cell == current or cell == neighbor or not cell.full

        x, y = current.coordinates
        offsets = [
                    (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                    (x - 1, y), (x, y), (x + 1, y),
                    (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
                   ]
        cell_less_wall = 0
        for cordinate in offsets:
            if is_valid(cordinate):
                check_n = self.maze.get_cell(cordinate)
                if len(check_n.get_walls()) <= 2:
                    cell_less_wall += 1
        if cell_less_wall >= 9:
            return False
        return True

    def break_walls(self) -> None:
        h = self.maze.height
        w = self.maze.width
        r = (h * w)

        for _ in range(r):
            x = self.rng.randint(0, w - 1)
            y = self.rng.randint(0, h - 1)

            current = self.maze.get_cell((x, y))
            if current.full:
                continue
            neighbours = [
                (x, y - 1), (x + 1, y),
                (x, y + 1), (x - 1, y)
            ]
            neighbour_pos = self.rng.choice(neighbours)
            if not self.check_cordinate_in_range(neighbour_pos):
                continue
            neighbour = self.maze.get_cell(neighbour_pos)
            if neighbour.full:
                continue
            if self.can_break_wall(current, neighbour):
                self.maze.add_connection(current.coordinates, neighbour_pos)

    def generate(self) -> None:
        """ Generates a maze with the 42 pattern in the center. If the exit
            overlaps with the pattern, moves the exit down one cell and
            repeats """
        try:
            self.maze.append_pattern()
            x, y = self.maze.start
            self.create_paths(self.maze[y][x])
            return
        except ValueError:
            x = self.maze.end[0]
            y = self.maze.end[1] + 1
            self.maze.end = (x, y)
            self.generate()

    @classmethod
    def create_instance(cls: Type[T_GENERATE], config: dict) -> T_GENERATE:
        generator = cls()

        height = config["HEIGHT"]
        width = config["WIDTH"]
        start = config["ENTRY"]
        end = config["EXIT"]
        perfect = config["PERFECT"]
        seed = config["SEED"]

        generator.maze = Maze(width, height, start, end)

        if seed == 0:
            seed = None
        generator.seed = seed

        generator.generate()

        if not perfect:
            generator.break_walls()

        return generator


def create_new_maze(config: dict) -> Maze:
    """Generates a new maze using the current configuration, and writes its
    data to the output file"""
    try:
        is_valid_config(config)
    except ValueError as e:
        raise ValueError("Error creating maze - received invalid config:"
                         f"\n{e}")
    maze_gen = MazeGenerator.create_instance(config)
    write_maze_to_file(config, maze_gen.maze)

    return maze_gen.maze

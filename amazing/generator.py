import sys
import random
from .cell import Cell
from .maze import Maze
from .file_handler import write_maze_to_file


class MazeGenerator():
    def __init__(self, maze: Maze, seed: str = None) -> None:
        sys.setrecursionlimit(10_000)
        self.maze = maze
        self.seed = seed
        self.stack = []
        self.__seed = None
        self.seed = seed
        self.__rng = random.Random(self.seed)

    @property
    def maze(self) -> Maze:
        return self.__maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        self.__maze = maze

    @property
    def seed(self) -> int:
        return self.__seed

    @seed.setter
    def seed(self, seed: int) -> None:
        self.__seed = seed

    @property
    def stack(self) -> list[Cell]:
        return self.__stack

    @stack.setter
    def stack(self, stack: list[Cell]) -> None:
        self.__stack = stack

    @property
    def seed(self) -> str:
        return self.__seed

    @seed.setter
    def seed(self, seed: str) -> None:
        try:
            if seed:
                self.__seed = str(seed)
        except TypeError:
            print("Error: Seed must be int or str")

    @property
    def rng(self) -> random.Random():
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
        def is_valid(cordinate):
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

    def break_wall(self):
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
            if self.seed != 0:
                random.seed(self.seed)
            self.maze.append_pattern()
            x, y = self.maze.start
            self.create_paths(self.maze[y][x])
            return
        except ValueError:
            x = self.maze.end[0]
            y = self.maze.end[1] + 1
            self.maze.end = (x, y)
            self.generate()


def create_new_maze(config: dict) -> Maze:
    """ Generates a new maze using the current configuration, and writes its
        data to the output file """
    height = config["HEIGHT"]
    width = config["WIDTH"]
    start = config["ENTRY"]
    end = config["EXIT"]
    seed = config["SEED"]
    perfect = config["PERFECT"]
    if seed == 0:
        seed = None

    maze = Maze(width, height, start, end)
    maze_gen = MazeGenerator(maze, seed)
    maze_gen = MazeGenerator(maze, seed)
    maze_gen.generate()
    if not perfect:
        maze_gen.break_wall()

    write_maze_to_file(config, maze)
    return maze

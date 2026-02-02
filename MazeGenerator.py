import sys
import random
from Cell import Cell
from Maze import Maze


class MazeGenerator():
    def __init__(self, maze: Maze) -> None:
        sys.setrecursionlimit(10_000)
        self.__maze = maze
        self.maze = maze
        self.__stack = []

    @property
    def maze(self) -> Maze:
        return self.__maze

    @property
    def stack(self) -> list:
        return self.__stack

    @maze.setter
    def maze(self, maze: Maze) -> None:
        self.__maze = maze

    def check_cordinate_in_range(self, cordinate: tuple) -> bool:
        x, y = cordinate
        if x < 0 or x >= self.maze.width:
            return False
        if y < 0 or y >= self.maze.height:
            return False
        return True

    def pop_stack(self) -> Cell:
        return self.__stack.pop()

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
            return random.choice(neighbours)
        return None

    def generate_maze(self, current: Cell) -> None:
        current.visited = True
        next_cell = self.check_neighbours(current)
        if next_cell:
            next_cell.visited = True
            self.push_stack(current)
            self.maze.add_connection(current.cordinate, next_cell.cordinate)
            self.generate_maze(next_cell)
        elif len(self.stack) > 0:
            self.generate_maze(self.pop_stack())

    def generate(self) -> None:
        self.maze.append_patern()
        x, y = self.maze.start
        self.generate_maze(self.maze[y][x])

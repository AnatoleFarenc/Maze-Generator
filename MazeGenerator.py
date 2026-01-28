from Maze import Maze
import random
from Showcase import Showcase
from Cell import Cell
import sys

sys.setrecursionlimit(10_000)

class MazeGenerator():
    def __init__(self, maze: Maze) -> None:
        self.__maze = maze
        self.maze = maze
        self.__stack = []

    @property
    def maze(self) -> Maze:
        return self.__maze

    @property
    def check_grid(self) -> list[list]:
        return self.__check_grid

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
        self.__stack.insert(0, cell)

    def check_neighbours(self, current: Cell) -> Cell | None:
        neighbours = []

        neighbour = {
            'top': (current.x, current.y - 1),
            'right': (current.x + 1, current.y),
            'bot': (current.x, current.y + 1),
            'left': (current.x - 1, current.y)
        }

        for key, value in neighbour.items():
            if self.check_cordinate_in_range(value):
                if self.maze[value[1]][value[0]].visited is False:
                    neighbours.append(self.maze[value[1]][value[0]])
        if len(neighbours) > 0:
            return random.choice(neighbours)
        return None

    def generate(self, current: Cell) -> None:
        current.visited = True
        next_cell = self.check_neighbours(current)
        if next_cell:
            next_cell.visited = True
            self.push_stack(current)
            self.maze.add_connection(current.cordinate, next_cell.cordinate)
            self.generate(next_cell)
        elif len(self.stack) > 0:
            self.generate(self.pop_stack())


def display_maze(grid) -> None:
    for line in grid:
        for cell in line:
            print(cell, end="")
        print()
    print()


def debug():
    display = Showcase()
    maze = Maze(20, 20, (0, 0), (10, 10))
    maze_gen = MazeGenerator(maze)
    # ascci_maze = display.generate_ascii_maze(maze)
    # display_maze(ascci_maze)
    # maze.debug_grid()
    # print()
    maze_gen.generate(maze[3][3])
    print()
    maze.debug_grid()
    ascci_maze = display.generate_ascii_maze(maze)
    display_maze(ascci_maze)


if __name__ == "__main__":
    debug()

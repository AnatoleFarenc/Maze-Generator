from Maze import Maze
from Cell import Cell
from typing import List, Any
from MazeGenerator import MazeGenerator


class PathFinding():
    def __init__(self, maze: Maze):
        self.__maze = None
        self.maze = maze
        self.__open = []
        self.__close = []

    @property
    def maze(self) -> Maze:
        return self.__maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        self.__maze = maze

    @property
    def open(self) -> List[Any]:
        return self.__open

    @property
    def close(self) -> List[Any]:
        return self.__close

    def get_neighbors(self, current: Cell) -> List[Cell]:
        neighbors_lst = []
        neighbors = current.get_value()
        # North
        if not ((neighbors >> 0) & 1):
            neighbors_lst.append(self.maze[current.y - 1][current.x])
        # East
        if not ((neighbors >> 1) & 1):
            neighbors_lst.append(self.maze[current.y][current.x + 1])
        # South
        if not ((neighbors >> 2) & 1):
            neighbors_lst.append(self.maze[current.y + 1][current.x])
        # Weast
        if not ((neighbors >> 3) & 1):
            neighbors_lst.append(self.maze[current.y][current.x - 1])
        return neighbors_lst

    def get_heuristique_path(self, current: Cell) -> int:
        x, y = current.cordinate
        x_end, y_end = self.maze.end
        # Manhattan distance
        return (abs(x - x_end) + abs(y - y_end))

    def find_exit(self, start: Cell) -> List[Any]:
        # Check if I've reached the end
        self.open.append(start)
        start.cost = 0
        start.parent = None
        start.g_h_cost = self.get_heuristique_path(start)

        while self.open:
            current = min(self.open, key=lambda cell: cell.g_h_cost)

            if current.cordinate == self.maze.end:
                path = []
                node = current
                while node:
                    path.append(node)
                    node = node.parent
                return path[::-1]

            # Add append cell to the close list
            self.open.remove(current)
            self.close.append(current)

            # Find the greater cell for the next path
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                g_value = current.cost + 1
                h_value = self.get_heuristique_path(neighbor)

                if neighbor in self.close:
                    continue

                if neighbor not in self.open:
                    # calcul cost: f=g+h
                    neighbor.cost = g_value
                    neighbor.g_h_cost = g_value + h_value
                    neighbor.parent = current
                    self.open.append(neighbor)
                else:
                    if neighbor.cost > g_value:
                        neighbor.cost = g_value
                        neighbor.g_h_cost = g_value + h_value
                        neighbor.parent = current
        return None

    def get_path_hex(self):
        x, y = self.maze.start
        path_cell_lst = self.find_exit(self.maze[y][x])
        path_hex = []
        for cell in path_cell_lst:
            path_hex.append(cell.get_hex_value())
        return path_hex


maze = Maze(5, 5, (0, 0), (3, 3))
maze_g = MazeGenerator(maze)
maze_g.generate()

from Showcase import Showcase
maze_style = Showcase.format_maze(maze, "ASCII")
Showcase.display_maze(maze_style, "ASCII", "WHITE", "RED")

path_f = PathFinding(maze)
x, y = maze.start
lst_cell = path_f.find_exit(maze[y][x])
for cell in lst_cell:
    print(cell.cordinate)

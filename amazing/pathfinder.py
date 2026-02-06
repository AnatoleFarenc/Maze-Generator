from typing import Any, List
from .maze import Maze
from .cell import Cell


class Pathfinder():
    def __init__(self, maze: Maze):
        self.__maze: Maze = maze
        self.__open: List[Cell] = []
        self.__close: List[Cell] = []
        self.start = self.maze.get_cell(maze.start)
        self.end = self.maze.get_cell(maze.end)

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

    @property
    def start(self) -> Cell:
        return self.__start

    @start.setter
    def start(self, n_start: Cell) -> None:
        self.__start = n_start

    @property
    def end(self) -> Cell:
        return self.__end

    @end.setter
    def end(self, n_end: Cell) -> None:
        self.__end = n_end

    def get_neighbors(self, current: Cell) -> List[Cell]:
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
        x, y = current.coordinates
        x_end, y_end = self.maze.end

        # Manhattan distance
        return (int(abs(x - x_end) + abs(y - y_end)))

    def find_exit(self) -> List[Cell]:
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

            # Add append cell to the close list
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
        path_cell_list = self.find_exit()

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
        direction_string = ""
        for dir in self.get_directions():
            direction_string += dir

        return direction_string


if __name__ == "__main__":
    from .generator import MazeGenerator
    from .showcase import format_maze, display_maze

    maze = Maze(5, 5, (0, 0), (3, 3))
    maze_g = MazeGenerator(maze, 0)
    maze_g.generate()

    maze_style = format_maze(maze, None, "ASCII")
    display_maze(maze_style, "ASCII", ("WHITE", "RED", "BLUE"))

    path_f = Pathfinder(maze)
    lst_cell = path_f.find_exit()
    for cell in lst_cell:
        print(cell.coordinates)

    directions = path_f.get_directions()
    print(directions)

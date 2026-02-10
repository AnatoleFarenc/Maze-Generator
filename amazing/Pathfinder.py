from typing import Any, List
from .Maze import Maze
from .Cell import Cell


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

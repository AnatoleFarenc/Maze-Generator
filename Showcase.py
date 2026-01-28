from Maze import Maze


class Showcase():
    @classmethod
    def generate_grid(cls, maze: Maze) -> list[list[str]]:
        rows = (maze.height * 2) + 1
        columns = (maze.width * 4) + 1
        display = [[' ' for j in range(columns)] for i in range(rows)]
        for row in range(rows):
            for col in range(columns):
                if row % 2 == 0:
                    display[row][col] = '+' if col % 4 == 0 else '-'
                else:
                    display[row][col] = '|' if col % 4 == 0 else ' '
        return display

    @classmethod
    def generate_ascii_maze(cls, maze: Maze) -> list[list[str]]:
        height = maze.height
        width = maze.width
        display = cls.generate_grid(maze)
        for row in range(height):
            for col in range(width):
                cell_walls = maze[row][col].get_walls()
                if "North" not in cell_walls:
                    grid_x = (col * 4) + 1
                    grid_y = (row * 2)
                    for k in range(3):
                        display[grid_y][grid_x + k] = ' '
                if "East" not in cell_walls:
                    grid_x = (col * 4) + 4
                    grid_y = (row * 2) + 1
                    display[grid_y][grid_x] = ' '
                if "South" not in cell_walls:
                    grid_x = (col * 4) + 1
                    grid_y = (row * 2) + 2
                    for k in range(3):
                        display[grid_y][grid_x + k] = ' '
                if "West" not in cell_walls:
                    grid_x = (col * 4) + 2
                    grid_y = (row * 2) + 1
                    display[grid_y][grid_x] = ' '
        return display

# Mini maze example:
# +----+----+----+
# |         |    |
# +    +    +    +
# |    |         |
# +    +----+    +
# |         |    |
# +----+----+----+

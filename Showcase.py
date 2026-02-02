from Maze import Maze
from copy import deepcopy


def is_horiz(c):
    return c in ('-', '+')


def is_vert(c):
    return c in ('|', '+')


class Showcase():
    @classmethod
    def generate_grid(cls, maze: Maze, style: str) -> list[list[str]]:
        rows = (maze.height * 2) + 1
        columns = (maze.width * 4) + 1
        display = [[' ' for _ in range(columns)] for _ in range(rows)]

        if style == "BLOCK":
            for row in range(rows):
                for col in range(columns):
                    if row % 2 == 0:
                        display[row][col] = "█"
                    else:
                        display[row][col] = "█" if col % 4 == 0 else ' '
        else:
            for row in range(rows):
                for col in range(columns):
                    if row % 2 == 0:
                        display[row][col] = '+' if col % 4 == 0 else '-'
                    else:
                        display[row][col] = '|' if col % 4 == 0 else ' '
        return display

    @classmethod
    def unicode_conversion(cls, display: list[list[str]]):
        rows = len(display)
        cols = len(display[0])
        copy = deepcopy(display)

        for y in range(rows):
            for x in range(cols):
                if copy[y][x] in ('+', '|', '-'):
                    up = (y > 0) and is_vert(copy[y-1][x])
                    down = (y < rows - 1) and is_vert(copy[y+1][x])
                    left = (x > 0) and is_horiz(copy[y][x-1])
                    right = (x < cols - 1) and is_horiz(copy[y][x+1])
                    if up and down and left and right:
                        display[y][x] = '┼'
                    elif down and left and right:
                        display[y][x] = '┬'
                    elif up and left and right:
                        display[y][x] = '┴'
                    elif up and down and right:
                        display[y][x] = '├'
                    elif up and down and left:
                        display[y][x] = '┤'
                    elif down and right:
                        display[y][x] = '┌'
                    elif down and left:
                        display[y][x] = '┐'
                    elif up and right:
                        display[y][x] = '└'
                    elif up and left:
                        display[y][x] = '┘'
                    elif up or down:
                        display[y][x] = '│'
                    elif left or right:
                        display[y][x] = '─'

    @classmethod
    def block_conversion(cls, display: list[list[str]]):
        rows = len(display)
        cols = len(display[0])

        for row in range(rows):
            for col in range(cols):
                if row == 0:
                    if display[row + 1][col] == '█':
                        display[row][col] = '█'
                    else:
                        display[row][col] = '▀'
                elif row < rows - 1:
                    if display[row][col] == '█':
                        if (display[row + 1][col] == " "):
                            display[row][col] = '▀'
                else:
                    display[row][col] = '▀'

    @classmethod
    def format_maze(cls, maze: Maze, style: str) -> list[list[str]]:
        height = maze.height
        width = maze.width
        display = cls.generate_grid(maze, style)
        # Remove walls in the grid to match the maze cells
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

        # Set the start and end symbol
        if style == "UNICODE":
            cls.unicode_conversion(display)
        elif style == "BLOCK":
            cls.block_conversion(display)

        # Mark the start and end cells
        start_row = (maze.start[1] * 2) + 1
        start_col = (maze.start[0] * 4) + 2
        end_row = (maze.end[1] * 2) + 1
        end_col = (maze.end[0] * 4) + 2

        display[start_row][start_col] = 'o'
        display[end_row][end_col] = 'o'
        return display

    @classmethod
    def format_game_maze(cls, maze: Maze, player: tuple) -> list[list[str]]:
        height = maze.height
        width = maze.width
        display = cls.generate_grid(maze, "BLOCK")
        # Remove walls in the grid to match the maze cells
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

        cls.block_conversion(display)

        # Mark the start and end cells
        start_row = (maze.start[1] * 2) + 1
        start_col = (maze.start[0] * 4) + 2
        end_row = (maze.end[1] * 2) + 1
        end_col = (maze.end[0] * 4) + 2

        display[start_row][start_col] = 'o'
        display[end_row][end_col] = 'o'

        # Mark the player position
        player_row = (player[1] * 2) + 1
        player_col = (player[0] * 4) + 2
        display[player_row][player_col] = '@'

        return display

    @classmethod
    def display_maze(cls, grid, style, w_color, o_color) -> None:
        """ Displays the maze on the terminal """
        print(f"\nMaze ({style} format):")
        match w_color:
            case "WHITE":
                w_color = "\033[0m"
            case "RED":
                w_color = "\033[31m"
            case "GREEN":
                w_color = "\033[32m"
            case "BLUE":
                w_color = "\033[94m"
            case "YELLOW":
                w_color = "\033[33m"
            case "PURPLE":
                w_color = "\033[35m"
        match o_color:
            case "WHITE":
                o_color = "\033[0m"
            case "RED":
                o_color = "\033[31m"
            case "GREEN":
                o_color = "\033[32m"
            case "BLUE":
                o_color = "\033[94m"
            case "YELLOW":
                o_color = "\033[33m"
            case "PURPLE":
                o_color = "\033[35m"
        point = 'o'
        if style == "UNICODE":
            point = '●'
        elif style == "BLOCK":
            point = '▀'

        for line in grid:
            for cell in line:
                if cell == ' ':
                    print(cell, end="")
                elif cell == 'o':
                    print(f"{o_color}{point}\033[0m", end="")
                else:
                    print(f"{w_color}{cell}\033[0m", end="")
            print()
        print()

    @classmethod
    def display_game_maze(cls, grid, player_pos, w_color, o_color) -> None:
        """ Displays the maze on the terminal """
        match w_color:
            case "WHITE":
                w_color = "\033[0m"
            case "RED":
                w_color = "\033[31m"
            case "GREEN":
                w_color = "\033[32m"
            case "BLUE":
                w_color = "\033[94m"
            case "YELLOW":
                w_color = "\033[33m"
            case "PURPLE":
                w_color = "\033[35m"
        match o_color:
            case "WHITE":
                o_color = "\033[0m"
            case "RED":
                o_color = "\033[31m"
            case "GREEN":
                o_color = "\033[32m"
            case "BLUE":
                o_color = "\033[94m"
            case "YELLOW":
                o_color = "\033[33m"
            case "PURPLE":
                o_color = "\033[35m"
        p_color = "\033[34m"

        point = '▀'
        for line in grid:
            for cell in line:
                if cell == ' ':
                    print(cell, end="")
                elif cell == 'o':
                    print(f"{o_color}{point}\033[0m", end="")
                elif cell == '@':
                    print(f"{p_color}{point}\033[0m", end="")
                else:
                    print(f"{w_color}{cell}\033[0m", end="")
            print()
        print("Use WASD to move! (or '0' to exit)")

# Mini maze example:
# +----+----+----+
# |         |    |
# +    +    +    +
# |    |         |
# +    +----+    +
# |         |    |
# +----+----+----+

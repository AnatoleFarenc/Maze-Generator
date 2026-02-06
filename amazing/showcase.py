from time import sleep
from copy import deepcopy
from typing import Optional
from os import system as console
from .Cell import Cell
from .Maze import Maze
from .Pathfinder import Pathfinder


def is_horizontal(c: str) -> bool:
    return c in ('-', '+')


def is_vertical(c: str) -> bool:
    return c in ('|', '+')


def is_full(cell: Cell) -> bool:
    return len(cell.get_walls()) == 4


def get_color_code(color: str) -> str:
    match color:
        case "WHITE":
            color = "\033[0m"
        case "RED":
            color = "\033[31m"
        case "GREEN":
            color = "\033[32m"
        case "BLUE":
            color = "\033[94m"
        case "YELLOW":
            color = "\033[33m"
        case "PURPLE":
            color = "\033[35m"
        case _:
            raise ValueError(f"Error getting color - Invalid value '{color}'")

    return color


def get_crumb_color(color: str) -> str:
    match color:
        case "WHITE":
            color = "\033[38;5;248m"
        case "RED":
            color = "\033[38;5;203m"
        case "GREEN":
            color = "\033[38;5;155m"
        case "BLUE":
            color = "\033[38;5;68m"
        case "YELLOW":
            color = "\033[38;5;221m"
        case "PURPLE":
            color = "\033[38;5;219m"
        case _:
            raise ValueError(f"Error getting color - Invalid value '{color}'")

    return color


def add_background(display: list[list[str]], cell: Cell, style: str) -> None:
    row = (cell.y * 2)
    col = (cell.x * 4)
    if style == "BLOCK":
        for r in range(2):
            for c in range(5):
                display[row + r][col + c] = '█'
    elif style == "ASCII":
        for r in range(3):
            for c in range(5):
                display[row + r][col + c] = '+'
    elif style == "UNICODE":
        for c in range(1, 4):
            display[row + 1][col + c] = '█'


def generate_grid(maze: Maze, style: str) -> list[list[str]]:
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


def unicode_conversion(display: list[list[str]]) -> None:
    rows = len(display)
    cols = len(display[0])
    copy = deepcopy(display)

    for y in range(rows):
        for x in range(cols):
            if copy[y][x] in ('+', '|', '-'):
                up = (y > 0) and is_vertical(copy[y-1][x])
                down = (y < rows - 1) and is_vertical(copy[y+1][x])
                left = (x > 0) and is_horizontal(copy[y][x-1])
                right = (x < cols - 1) and is_horizontal(copy[y][x+1])
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


def block_conversion(display: list[list[str]]) -> None:
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


def add_crumb(display: list[list[str]], camp: tuple, explorer: tuple) -> None:
    camp_row = (camp[1] * 2) + 1
    camp_col = (camp[0] * 4) + 2

    explorer_row = (explorer[1] * 2) + 1
    explorer_col = (explorer[0] * 4) + 2

    if explorer_row > camp_row:
        for row in range(camp_row, explorer_row + 1):
            if display[row][explorer_col] == ' ':
                display[row][explorer_col] = 'c'
    elif explorer_row < camp_row:
        for row in range(explorer_row, camp_row + 1):
            if display[row][explorer_col] == ' ':
                display[row][explorer_col] = 'c'
    elif explorer_col > camp_col:
        for col in range(camp_col, explorer_col + 1):
            if col % 2 == 0 and display[explorer_row][col] == ' ':
                display[explorer_row][col] = 'c'
    elif explorer_col < camp_col:
        for col in range(explorer_col, camp_col + 1):
            if col % 2 == 0 and display[explorer_row][col] == ' ':
                display[explorer_row][col] = 'c'


def format_maze(maze: Maze, player: Optional[tuple],
                style: str) -> list[list[str]]:
    height = maze.height
    width = maze.width
    display = generate_grid(maze, style)

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

    if style == "UNICODE":
        unicode_conversion(display)
    elif style == "BLOCK":
        block_conversion(display)

    start_row = (maze.start[1] * 2) + 1
    start_col = (maze.start[0] * 4) + 2
    end_row = (maze.end[1] * 2) + 1
    end_col = (maze.end[0] * 4) + 2

    display[start_row][start_col] = 'o'
    display[end_row][end_col] = 'o'

    if player is not None:
        display[(player[1] * 2) + 1][(player[0] * 4) + 2] = '@'

    for line in maze:
        for cell in line:
            if is_full(cell):
                add_background(display, cell, style)

    return display


def display_maze(grid: list[list[str]], style: str,
                 colors: tuple[str, str, str]) -> None:
    """ Displays the maze on the terminal """
    w_color = get_color_code(colors[0])
    o_color = get_color_code(colors[1])
    p_color = get_crumb_color(colors[2])

    if style == "ASCII":
        objective = 'o'
        crumb = '+'
    elif style == "UNICODE":
        objective = '●'
        crumb = '●'
    else:
        objective = '▀'
        crumb = '▀'

    for line in grid:
        for cell in line:
            if cell == ' ':
                print(cell, end="")
            elif cell == 'o':
                print(f"{o_color}{objective}\033[0m", end="")
            elif cell == '@':
                print(f"{p_color}{objective}\033[0m", end="")
            elif cell == 'c':
                print(f"{p_color}{crumb}\033[0m", end="")
            else:
                print(f"{w_color}{cell}\033[0m", end="")
        print()


def display_path(maze: Maze, style: str, colors: tuple[str, str, str]
                 ) -> list[list[str]]:
    pathfinder = Pathfinder(maze)
    directions = pathfinder.get_directions()

    explorer = pathfinder.start.coordinates

    display = format_maze(maze, None, style)

    for direction in directions:
        console("clear")
        print("=== A-Maze-ing ===")
        camp = explorer
        x, y = explorer
        match direction:
            case "N":
                explorer = (x, y - 1)
            case "E":
                explorer = (x + 1, y)
            case "S":
                explorer = (x, y + 1)
            case "W":
                explorer = (x - 1, y)
            case _:
                raise ValueError("Error displaying path - Received invalid "
                                 "direction")

        if explorer != pathfinder.start.coordinates:
            add_crumb(display, camp, explorer)
        display_maze(display, style, colors)
        sleep(0.075)

    return display

# Mini maze example:
# +----+----+----+
# |         |    |
# +    +    +    +
# |    |         |
# +    +----+    +
# |         |    |
# +----+----+----+

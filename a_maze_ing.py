import sys
from os import path
from Maze import Maze
from Showcase import Showcase
from parser import get_config
from os import remove as delete
from user_interface import input_loop


def test(config: dict) -> None:
    height = config["HEIGHT"]
    width = config["WIDTH"]
    start = config["ENTRY"]
    end = config["EXIT"]
    maze = Maze(width, height, start, end)
    maze.add_connection((0, 0), (1, 0))
    maze.add_connection((1, 0), (1, 1))
    maze.add_connection((1, 1), (1, 2))
    maze.add_connection((1, 2), (0, 2))
    maze.add_connection((0, 2), (0, 1))

    maze.add_connection((1, 0), (2, 0))
    maze.add_connection((2, 0), (2, 1))
    maze.add_connection((2, 1), (2, 2))

    maze.debug_grid()
    print()

    display = Showcase
    grid = display.generate_ascii_maze(maze)
    for line in grid:
        for cell in line:
            print(cell, end="")
        print()
    print()


def main():
    try:
        args = sys.argv
        if len(args) != 2:
            raise ValueError("Error: could not execute file - Invalid input: "
                             f"{args[1:]}\nExpected command: "
                             "python3 a_maze_ing.py [config file]")
        config = get_config(args[1])
    except ValueError as e:
        print(f"Error occurred while accessing config file\n{e}")
        return
    if path.exists(config["OUTPUT_FILE"]):
        delete(config["OUTPUT_FILE"])
    input_loop(config)


if __name__ == "__main__":
    main()

from os import system as console
from copy import deepcopy
from Maze import Maze
from Showcase import Showcase
from MazeGenerator import MazeGenerator, display_maze
from parser import process_key_value_pair
from parser import display_config, is_valid_config


def display_options(options: dict):
    print("Options:")
    for key, value in options.items():
        print(f"{key}. {value}")


def create_new_maze(config: dict) -> list[list[str]]:
    height = config["HEIGHT"]
    width = config["WIDTH"]
    start = config["ENTRY"]
    end = config["EXIT"]
    maze = Maze(width, height, start, end)
    maze_gen = MazeGenerator(maze)
    maze_gen.generate(maze.start)
    ascii_maze = Showcase.generate_ascii_maze(maze)

    output_file = config["OUTPUT_FILE"]
    output_data = ""
    for row in maze:
        for cell in row:
            output_data += str(cell)
        output_data += '\n'
    with open(output_file, "w") as fd:
        fd.write(output_data)
        fd.write('\n')
        fd.write(f"{start[0]},{start[1]}")
        fd.write('\n')
        fd.write(f"{end[0]},{end[1]}")
    return ascii_maze


def modify_config(config: dict):
    display_config(config)
    print()
    key = None
    while key is None:
        user_input = input("Enter the key to change: ")
        if user_input.upper() in config:
            key = user_input.upper()
        else:
            print("\033[F\033[K", end="")
            print("\033[F\033[K", end="")
            print("Error: Key does not exist")

    print("\033[F\033[K", end="")
    print("\033[F\033[K")
    value = None
    while value is None:
        user_input = input("Enter the new value: ")
        test_config = deepcopy(config)
        try:
            processed_value = process_key_value_pair(key, user_input)
            test_config[key] = processed_value
            is_valid_config(test_config)
            value = processed_value
        except ValueError as e:
            print("\033[F\033[K", end="")
            print("\033[F\033[K", end="")
            print(e)
    config[key] = value


def show_maze_data(file: str):
    try:
        with open(file, "r") as fd:
            data = fd.read()
            print("Maze data:")
            print(data)
    except FileNotFoundError:
        print("You haven't created a maze yet!")
        print("First, select the 'Generate maze' option, then come back :)")
        print()


def input_loop(config: dict):
    choice = None
    system_message = ''
    options = {1: "Generate maze",
               2: "Show config",
               3: "Modify config",
               4: "Show maze data",
               0: "Exit... :("}
    while True:
        console("clear")
        print("=== A-Maze-ing ===\n\n")
        if choice is not None:
            match choice:
                case 1:
                    new_maze = create_new_maze(config)
                    display_maze(new_maze)
                case 2:
                    display_config(config)
                case 3:
                    modify_config(config)
                    choice = None
                    continue
                case 4:
                    show_maze_data(config["OUTPUT_FILE"])
        display_options(options)
        print(system_message)
        try:
            user_input = int(input("> "))
            if (user_input == 0):
                return
            if (user_input in options):
                choice = user_input
            else:
                choice = None
                system_message = ("Invalid input. Please enter a number "
                                  f"from 0-{len(options) - 1}")
        except ValueError:
            choice = None
            system_message = ("Invalid input. Please enter a number "
                              f"from 0-{len(options) - 1}")

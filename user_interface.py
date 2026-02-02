from os import system as console
from copy import deepcopy
from Maze import Maze
from Showcase import Showcase
from MazeGenerator import MazeGenerator
from parser import process_key_value_pair
from parser import display_config, is_valid_config
from minigame import game_loop


def display_options(options: dict):
    """ Displays options menu """
    print("\nOptions:")
    for key, value in options.items():
        print(f"{key}. {value}")


def create_new_maze(config: dict) -> Maze:
    """ Generates a new maze using the current configuration, and writes its
        data to the output file """
    height = config["HEIGHT"]
    width = config["WIDTH"]
    start = config["ENTRY"]
    end = config["EXIT"]
    maze = Maze(width, height, start, end)
    maze_gen = MazeGenerator(maze)
    maze_gen.generate()

    output_file = config["OUTPUT_FILE"]
    output_data = ""
    for row in maze:
        for cell in row:
            output_data += cell.get_hex_value()
        output_data += '\n'
    with open(output_file, "w") as fd:
        fd.write(output_data)
        fd.write('\n')
        fd.write(f"{start[0]},{start[1]}")
        fd.write('\n')
        fd.write(f"{end[0]},{end[1]}")
    return maze


def config_menu(config: dict):
    """ Displays the config data and allows the user to modify the values """
    system_message = ""

    while True:
        key = None
        while key is None:
            console("clear")
            print("=== Config Menu ===\n")
            display_config(config)
            print("Type 'Done' to exit")
            if system_message:
                print(system_message)
            user_input = input("Enter the key to change: ").strip().upper()
            if user_input in config:
                key = user_input
                system_message = ""
            elif user_input == "DONE":
                return
            else:
                system_message = f"Error: Key '{user_input}' does not exist"

        value = None
        while value is None:
            console("clear")
            print("=== Config Menu ===\n")
            display_config(config)
            print("Type 'Done' to exit")
            print(f"Selected key: {key}")
            if system_message:
                print(system_message)
            user_input = input("Enter the new value: ").strip()
            if user_input.upper() == "DONE":
                return
            test_config = deepcopy(config)
            try:
                processed_value = process_key_value_pair(key, user_input)
                test_config[key] = processed_value
                is_valid_config(test_config)
                value = processed_value
            except ValueError as e:
                system_message = e
        config[key] = value
        system_message = f"Key {key} set to {processed_value}"


def show_maze_data(file: str):
    """ Displays the output file data """
    try:
        with open(file, "r") as fd:
            data = fd.read()
            print("\nRaw maze data:")
            print(data)
            print()
    except FileNotFoundError:
        return ("You haven't created a maze yet!\nFirst, select the "
                "'Generate new maze' option, then come back :)")
    return ("")


def input_loop(config: dict):
    """ Starts the main program loop """
    choice = None
    maze = None
    maze_style = None
    style = "ASCII"
    system_message = ''
    options = {1: "Generate new maze",
               2: "Toggle maze format",
               3: "Show maze data",
               4: "Show config",
               5: "Modify config",
               6: "Play minigame :)",
               0: "Exit"}
    while True:
        console("clear")
        print("=== A-Maze-ing ===")
        if maze is None:
            print(f"\nMaze ({style} format):")
            print("The generated maze will appear here!")
        else:
            w_color = config["WALLS"]
            o_color = config["OBJECTIVES"]
            Showcase.display_maze(maze_style, style, w_color, o_color)
        if choice is not None:
            match choice:
                case 1:
                    maze = create_new_maze(config)
                    maze_style = Showcase.format_maze(maze, style)
                    system_message = "Maze created successfully!"
                    choice = None
                    continue
                case 2:
                    if style == "ASCII":
                        style = "UNICODE"
                    elif style == "UNICODE":
                        style = "BLOCK"
                    else:
                        style = "ASCII"
                    if maze is not None:
                        maze_style = Showcase.format_maze(maze, style)
                    choice = None
                    system_message = ""
                    continue
                case 3:
                    system_message = show_maze_data(config["OUTPUT_FILE"])
                case 4:
                    print("\nConfig:")
                    system_message = ""
                    display_config(config)
                case 5:
                    config_menu(config)
                    choice = None
                    system_message = "Config saved!"
                    continue
                case 6:
                    game_loop(config)
                    choice = None
                    system_message = ""
                    continue
        display_options(options)
        print(f"\n{system_message}")
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

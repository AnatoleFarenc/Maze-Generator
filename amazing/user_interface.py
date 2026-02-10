import random
from copy import deepcopy
from os import system as console
from .minigame import game_loop
from .parser import display_config
from .Generator import create_new_maze
from .config_handler import config_menu
from .file_handler import show_maze_data
from .showcase import format_maze, display_maze, display_path


def display_options(options: dict) -> None:
    """ Displays options menu """
    print("\nOptions:")
    for key, value in options.items():
        print(f"{key}. {value}")


def input_loop(config: dict) -> None:
    """ Starts the main program loop """
    choice = None
    maze = None
    maze_style = None
    unexplored = None
    style = "BLOCK"
    system_message = ''
    color_list = ["WHITE", "RED", "GREEN", "BLUE", "YELLOW", "PURPLE"]
    options = {1: "Generate new maze",
               2: "Show path",
               3: "Toggle maze format",
               4: "Randomize colors",
               5: "Show maze data",
               6: "Show config",
               7: "Modify config",
               8: "Play minigame :)",
               0: "Exit"}
    while True:
        console("clear")
        print("=== A-Maze-ing ===")
        print(f"\nMaze ({style} format):")
        if maze is None:
            print("The generated maze will appear here!")
        else:
            assert maze_style is not None
            w_color = config["WALLS"]
            o_color = config["OBJECTIVES"]
            p_color = config["PATH"]
            colors: tuple[str, str, str] = (w_color, o_color, p_color)
            display_maze(maze_style, style, colors)
            print()
        if choice is not None:
            match choice:
                case 1:
                    try:
                        maze = create_new_maze(config)
                        maze_style = format_maze(maze, style)
                        system_message = "Maze created successfully!"
                        if maze.height < 7 or maze.width < 9:
                            system_message += ("\nHowever, its size does "
                                               "not allow for 42 pattern")
                        choice = None
                        options[2] = "Show path"
                        unexplored = None
                        continue
                    except ValueError as e:
                        choice = None
                        system_message = str(e)
                case 2:
                    if maze is None:
                        system_message = ("You haven't created a maze yet!\n"
                                          "First, select the 'Generate new"
                                          " maze' option, then come back :)")
                    else:
                        assert maze is not None
                        if options[2] == "Show path":
                            if unexplored is None:
                                unexplored = deepcopy(maze_style)
                                maze_style = display_path(maze, style, colors)
                            else:
                                unexplored, maze_style = maze_style, unexplored
                            options[2] = "Hide path"
                        else:
                            options[2] = "Show path"
                            unexplored, maze_style = maze_style, unexplored
                        system_message = ""
                        choice = None
                        continue
                case 3:
                    if style == "ASCII":
                        style = "UNICODE"
                    elif style == "UNICODE":
                        style = "BLOCK"
                    else:
                        style = "ASCII"
                    if maze is not None:
                        maze_style = format_maze(maze, style)
                    choice = None
                    options[2] = "Show path"
                    unexplored = None
                    system_message = ""
                    continue
                case 4:
                    config["WALLS"] = random.choice(color_list)
                    config["OBJECTIVES"] = random.choice(color_list)
                    config["PATH"] = random.choice(color_list)
                    system_message = "Colors randomized!"
                    choice = None
                    continue
                case 5:
                    system_message = show_maze_data(config["OUTPUT_FILE"])
                case 6:
                    print("\nConfig:")
                    system_message = ""
                    display_config(config)
                case 7:
                    config_menu(config)
                    choice = None
                    system_message = "Config saved!"
                    continue
                case 8:
                    game_loop(config, style)
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

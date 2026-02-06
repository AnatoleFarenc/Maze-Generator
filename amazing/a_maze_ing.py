import sys
from os import path
from os import remove as delete
from .parser import get_config
from .user_interface import input_loop


def main() -> None:
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

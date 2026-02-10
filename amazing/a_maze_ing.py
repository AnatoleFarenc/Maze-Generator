import sys
from .parser import get_config
from .user_interface import input_loop


def main() -> None:
    """ main function """
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
    input_loop(config)


if __name__ == "__main__":
    main()

from .maze import Maze
from .pathfinder import Pathfinder


def write_maze_to_file(config: dict, maze: Maze) -> None:
    output_file = config["OUTPUT_FILE"]
    start = config["ENTRY"]
    end = config["EXIT"]

    output_data = maze.get_hex_data()

    pathfinder = Pathfinder(maze)
    directions = pathfinder.get_direction_string()

    with open(output_file, "w") as fd:
        fd.write(output_data)
        fd.write('\n')
        fd.write(f"{start[0]},{start[1]}")
        fd.write('\n')
        fd.write(f"{end[0]},{end[1]}")
        fd.write('\n')
        fd.write(directions)


def show_maze_data(file: str) -> str:
    """ Displays the output file content """
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

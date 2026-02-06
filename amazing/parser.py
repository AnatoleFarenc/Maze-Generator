from typing import Union, Tuple, Dict


def parse_config(file: str) -> Dict[str, str]:
    """ Parses the given file line by line (excluding comments) then creates a
        dictionary containing each key/value pair"""
    raw_config = {}

    try:
        with open(file, "r") as data:
            for i, line in enumerate(data, start=1):
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    raw_config[key.strip().upper()] = value.strip()
    except (OSError, ValueError) as e:
        raise ValueError(f"Error reading config file : {e}\n"
                         f"Occured at line {i} in file: '{line}'")
    return (raw_config)


def process_key_value_pair(key: str, raw_value: str
                           ) -> Union[int, str, bool, tuple]:
    """ Converts the raw config value to the correct type """
    key = key.upper()
    if key in {"ENTRY", "EXIT"}:
        try:
            return tuple(map(int, raw_value.split(',')))
        except ValueError:
            raise ValueError(f"Error assigning value - '{raw_value}' is not "
                             f"a valid value for {key}.\nExpected format:"
                             "'0,0', '1,3', '9,5', etc...")
    if key in {"WALLS", "OBJECTIVES", "PATH"}:
        raw_value = raw_value.upper()
    if raw_value.isdigit():
        return int(raw_value)
    if raw_value.upper() == "TRUE":
        return True
    if raw_value.upper() == "FALSE":
        return False
    return raw_value


def process_config(raw_config: Dict[str, str]
                   ) -> Dict[str, Union[int, bool, str, Tuple[int, ...]]]:
    """ Processes each key's value and converts it to the relevant type\n
        ex: {'Exit': '19,14'} -> {'Exit': (19, 14)} """
    config: Dict[str, Union[int, bool, str, Tuple[int, ...]]] = {}
    for key, value in raw_config.items():
        config[key] = process_key_value_pair(key, value)
    return (config)


def is_valid_config(config: Dict) -> None:
    """ Checks that the config data contains all the mandatory keys,
        and that their values are correct """
    mandatory_keys = {"WIDTH", "HEIGHT", "ENTRY",
                      "EXIT", "OUTPUT_FILE", "PERFECT",
                      "SEED", "WALLS", "OBJECTIVES", "PATH"}
    # Checks that all the mandatory keys are in the dictionary
    for key in mandatory_keys:
        if key not in config:
            raise ValueError(f"Error parsing config file - Missing '{key}' "
                             "key")
    # Checks that the height and width values are integers
    for key in ("WIDTH", "HEIGHT"):
        if not isinstance(config[key], int):
            raise ValueError(f"Error parsing config file - '{config[key]}' is "
                             f"not a valid input for {key} (must be int)")
    # Checks that the maze means the minimum size requirements
    if config["WIDTH"] * config["HEIGHT"] < 4:
        raise ValueError("Error parsing config file - Maze of size "
                         f"{config['WIDTH']}x{config['HEIGHT']} is too small "
                         "(2x2 minimum)")
    # Checks that the Entry and Exit tuples contain exactly two integers
    for key in ("ENTRY", "EXIT"):
        if len(config[key]) != 2:
            raise ValueError(f"Error parsing config file - {key} must have "
                             f"exactly 2 values: {config[key]} is invalid")
        x, y = config[key]
        if x >= config["WIDTH"] or y >= config["HEIGHT"]:
            raise ValueError(f"Error parsing config file - {key} coordinates "
                             f"{config[key]} outside of range "
                             f"({config['WIDTH']-1},{config['HEIGHT']-1})")
        elif x < 0 or y < 0:
            raise ValueError(f"Error parsing config file - {key} coordinates "
                             f"{config[key]} must be positive")
    # Checks that the Entry and Exit are not on the same cell
    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("Error parsing config file - Entry and Exit cannot "
                         "occupy the same cell")
    # Checks that the config file is a plain text file (.txt)
    if not isinstance(config["OUTPUT_FILE"], str):
        raise ValueError("Error parsing config file - Invalid output_file "
                         f"name '{config['OUTPUT_FILE']}'")
    if not config["OUTPUT_FILE"].endswith(".txt"):
        raise ValueError("Error parsing config file - Invalid "
                         f"output_file extension '{config['OUTPUT_FILE']}'"
                         " (extension must be '.txt')")
    # Checks that the perfect value is a boolean
    if not isinstance(config["PERFECT"], bool):
        raise ValueError("Error parsing config file - Invalid 'Perfect' "
                         "key value\nMust be 'True' or 'False'")
    # Checks that the Seed value is an int
    if not isinstance(config["SEED"], int):
        raise ValueError(f"Error parsing config file - '{config['SEED']}' is "
                         f"not a valid input for 'SEED' (must be int)")
    # Checks that the Walls value is a string
    if not isinstance(config["WALLS"], str):
        raise ValueError("Error parsing config file - Invalid 'WALLS' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Objectives value is a string
    if not isinstance(config["OBJECTIVES"], str):
        raise ValueError("Error parsing config file - Invalid 'OBJECTIVES' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW")
    # Checks that the Path value is a string
    if not isinstance(config["PATH"], str):
        raise ValueError("Error parsing config file - Invalid 'PATH' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Walls value is a valid color
    if config["WALLS"].upper() not in {"WHITE", "RED", "GREEN",
                                       "BLUE", "YELLOW", "PURPLE"}:
        raise ValueError("Error parsing config file - Invalid 'WALLS' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW")
    # Checks that the Objectives value is a valid color
    if config["OBJECTIVES"].upper() not in {"WHITE", "RED", "GREEN",
                                            "BLUE", "YELLOW", "PURPLE"}:
        raise ValueError("Error parsing config file - Invalid 'OBJECTIVES' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")
    # Checks that the Path value is a valid color
    if config["PATH"].upper() not in {"WHITE", "RED", "GREEN",
                                      "BLUE", "YELLOW", "PURPLE"}:
        raise ValueError("Error parsing config file - Invalid 'PATH' "
                         "key value\nValid colors: WHITE, RED, GREEN, "
                         "BLUE, YELLOW, PURPLE")


def get_config(file: str) -> Dict:
    """ Reads the given config file and returns a dictionary containing
        the config data """
    raw_config = parse_config(file)
    config = process_config(raw_config)
    is_valid_config(config)
    return (config)


def display_config(config: Dict) -> None:
    """ Displays the config values on stdout """
    for key, value in config.items():
        print(f"- {key}: {value}")
    print()


if __name__ == "__main__":
    display_config(get_config("config.txt"))

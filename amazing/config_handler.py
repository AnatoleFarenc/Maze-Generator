from copy import deepcopy
from os import system as console
from .parser import display_config, process_key_value_pair, is_valid_config


def config_menu(config: dict) -> None:
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
                system_message = str(e)
        config[key] = value
        system_message = f"Key {key} set to {processed_value}"

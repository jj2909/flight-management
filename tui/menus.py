from create_db import DB
import sys
from tui.utils import dict_to_table
from tui.handlers import search_values, add_values, delete_values, update_values


def show_intro():
    print(
        """
------------------------------
   FLIGHT MANAGEMENT SYSTEM   
------------------------------
    """
    )


def _show_menu(name: str, menu_dict: dict):
    while True:
        print(f"\n-------- {name} Menu -------- ")
        print("Choose from one of the following:")
        for k, v in menu_dict.items():
            print(f"{k}: {v["name"]}")
        if name != "Main":
            print("b: Back to main menu")
        print("q: Quit")

        option = input("> ").strip().lower()
        if option == "b":
            main_menu()
        if option == "q":
            sys.exit(0)
        elif option in menu_dict:
            print(f"> Selected: {menu_dict[option]["name"]}")
            menu_dict[option]["function"]()
        else:
            print("Invalid option, try again.")


def main_menu(tables: list[type[DB]]) -> None:
    submenu = {
        "1": {"name": "View/edit table", "function": lambda t=tables: table_menu(t)},
        "2": {"name": "Settings", "function": settings_menu},
    }
    _show_menu("Main", submenu)


def table_menu(tables: list[type[DB]]) -> None:
    submenu = {
        f"{i+1}": {
            "name": table.__name__,
            "function": (lambda t=table: table_options(t)),
        }
        for i, table in enumerate(tables)
    }

    _show_menu("Table", submenu)


def table_options(table: type[DB]) -> None:
    submenu = {
        "1": {
            "name": "View table",
            "function": lambda t=table: dict_to_table(t.find()),
        },
        "2": {
            "name": "View table with details",
            "function": lambda t=table: dict_to_table(t.find_all_with_details()),
        },
        "3": {
            "name": "Search by",
            "function": lambda t=table: search_values(t),
        },
        "4": {
            "name": "Add",
            "function": lambda t=table: add_values(t),
        },
        "5": {
            "name": "Update",
            "function": lambda t=table: update_values(t),
        },
        "6": {
            "name": "Delete",
            "function": lambda t=table: delete_values(t),
        },
    }

    _show_menu(table.__name__, submenu)


def settings_menu():
    submenu = {
        "1": {"name": "Setting1", "function": lambda: print("TODO: setting1")},
        "2": {"name": "Setting2", "function": lambda: print("TODO: setting2")},
    }

    _show_menu("Settings", submenu)

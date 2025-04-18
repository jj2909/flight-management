from app.models.base_model import DB
import sys
from app.tui.utils import dict_to_table
from app.tui.handlers import search_values, add_values, delete_values, update_values, set_logging_setting, group_by
from app.base.logger import logger


class FlightMangement:

    def __init__(self, tables: list[type[DB]]):
        self.tables = tables
        self.logger = logger
        logger.disabled = True

    def run(self):
        self.show_intro()
        self.main_menu()

    def show_intro(self):
        print(
            """
------------------------------
   FLIGHT MANAGEMENT SYSTEM   
------------------------------
        """
        )

    def _show_menu(self, name: str, menu_dict: dict):
        while True:
            print(f"\n-------- {name} Menu -------- ")
            print("Choose from the following:")
            for k, v in menu_dict.items():
                print(f"[{k}] {v["name"]}")
            if name != "Main":
                print("[b] Back")
            print("[q] Quit")

            option = input("> ").strip().lower()
            if option == "b":
                return
            if option == "q":
                sys.exit(0)
            elif option in menu_dict:
                print(f"Selected: {menu_dict[option]["name"]}")
                menu_dict[option]["function"]()
            else:
                print("ERROR: Invalid option")

    def main_menu(self) -> None:
        submenu = {
            "1": {"name": "View/edit table", "function": self.table_menu},
            "2": {"name": "Settings", "function": self.settings_menu},
        }
        self._show_menu("Main", submenu)

    def table_menu(self) -> None:
        submenu = {
            f"{i+1}": {
                "name": table.__name__,
                "function": (lambda t=table: self.table_options(t)),
            }
            for i, table in enumerate(self.tables)
        }

        self._show_menu("Table", submenu)

    def table_options(self, table: type[DB]) -> None:
        submenu = {
            "1": {
                "name": "View table",
                "function": lambda: dict_to_table(table.find()),
            },
            "2": {
                "name": "View table with details",
                "function": lambda: dict_to_table(table.find_all_with_details()),
            },
            "3": {
                "name": "Search by",
                "function": lambda: search_values(table),
            },
            "4": {
                "name": "Group by",
                "function": lambda: group_by(table),
            },
            "5": {
                "name": "Add record",
                "function": lambda: add_values(table),
            },
            "6": {
                "name": "Update record/s",
                "function": lambda: update_values(table),
            },
            "7": {
                "name": "Delete record/s",
                "function": lambda: delete_values(table),
            },
        }

        self._show_menu(table.__name__, submenu)

    def settings_menu(self):
        submenu = {
            "1": {"name": "(In development) Set ON DELETE restrictions", "function": lambda: print("Not ready yet :(")},
            "2": {"name": "Turn dev logs on/off", "function": lambda: set_logging_setting(logger)},
        }

        self._show_menu("Settings", submenu)

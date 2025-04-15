import sys
from time import sleep
from tabulate import tabulate
from create_db import DB
from load import initiate, Aircrafts, Airports, Pilots, Flights

tables = [Aircrafts, Airports, Pilots, Flights]


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


def show_intro():
    print(
        """
------------------------------
   FLIGHT MANAGEMENT SYSTEM   
------------------------------
    """
    )


def main_menu():
    submenu = {
        "1": {"name": "View/edit table", "function": table_menu},
        "2": {"name": "Settings", "function": settings_menu},
    }
    _show_menu("Main", submenu)


def table_menu() -> type[DB] | None:
    submenu = {
        f"{i+1}": {
            "name": table.__name__,
            "function": (lambda t=table: table_handler(t)),
        }
        for i, table in enumerate(tables)
    }

    _show_menu("Table", submenu)


def table_handler(table: type[DB]):
    submenu = {
        "1": {
            "name": "View table",
            "function": lambda t=table: dict_to_table(t.find_all()),
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


def dict_to_table(d: dict) -> None:
    if d:
        header = d[0].keys()
        rows = [x.values() for x in d]
        print(tabulate(rows, header))
        sleep(0.3)
    else:
        print("> Empty query")


def search_values(table: type[DB]) -> None:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    while True:
        print(f"Columns available: {names}")
        key_input = input(f"Which column do you want to SEARCH on (e.g. {names[0]}): ")
        if key_input in names:
            filter_input = input(
                f"What list of values do you want to filter column {key_input} (e.g. 1,2,3): "
            )
            dict_to_table(
                table.find_by_id(
                    [x.strip() for x in filter_input.split(",")], key=key_input
                )
            )
            break
        else:
            print(f"> Not a valid column")


def add_values(table: type[DB]) -> None:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    types = [field.type.__name__ for field in fields]
    __TYPE_MAP = {
        "int": int,
        "str": str,
        "NoneType": lambda x: None,
        "float": float,
    }

    print(f"Columns to input: {names}")
    values = input(
        f"Enter the entry you would like to add with values separated by commas: "
    )
    values = [v.strip() for v in values.split(",")]
    values = [__TYPE_MAP[typ](val) for typ, val in zip(types, values)]

    table(*values).insert()
    print("> Successfully added entry")


def update_values(table: type[DB]) -> None:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    names.pop(0)
    key_input = input(f"Which {table.primary_key} do you want to update? (e.g. ???): ")
    print(f"Columns available: {names}")
    updated_data = input(
        f"{key_input}: enter the updated column:value seperated by a comma (e.g. {names[0]}:???) "
    )

    updated_data = [x.strip().split(":") for x in updated_data.split(",")]
    updated_data.append([table.primary_key, key_input])
    table.update_by_id(dict(updated_data))

    print("row updated")


def delete_values(table: type[DB]) -> None:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    while True:
        print(f"Columns available: {names}")
        key_input = input(
            f"Which column do you want to DELETE from (e.g. {names[0]}): "
        )
        if key_input in names:
            filter_input = input(
                f"What list of values do you want to DELETE in column {key_input} (e.g. 1,2,3): "
            )

            table.delete_by_id(
                [x.strip() for x in filter_input.split(",")], key=key_input
            )

            print("TODO: number of rows deleted: ??")

            break
        else:
            print(f"> Not a valid column")


if __name__ == "__main__":
    initiate()
    show_intro()
    main_menu()

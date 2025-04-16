from tui.utils import dict_to_table
from create_db import DB


def _get_conditions(table: type[DB]) -> list[dict]:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    print(f"Columns available: {names}")
    col = input("What column do you want to filter by?: ")
    operator = input("On what operator [=, !=, <, >, IN]: ")
    print(f"{col} {operator} ?")
    value = input("What value?: ")
    return [{"column": col, "operator": operator, "value": value}]


def search_values(table: type[DB]) -> None:
    conditions = _get_conditions(table)
    dict_to_table(table.find(conditions))


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
    while True:
        to_filter = (
            input(f"Do you want apply a filter to delete? (Y/N): ").strip().upper()
        )

        if to_filter == "Y":
            conditions = _get_conditions(table)
            count = table.delete(conditions)
            print(f"Number of rows deleted {count}.")
            break
        if to_filter == "N":
            response = (
                input(
                    f"Are you sure you want to delete all records in {table.__name__}? (Y/N): "
                )
                .strip()
                .upper()
            )
            if response == "Y":
                print(f"Deleting all records in {table.__name__}...")
                break
            else:
                continue

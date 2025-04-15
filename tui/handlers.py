from tui.utils import dict_to_table
from create_db import DB

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


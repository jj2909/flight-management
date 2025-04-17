from time import sleep
from app.tui.utils import dict_to_table
from app.models.base_model import DB


def _get_conditions(table: type[DB]) -> list[dict]:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    print(f"Columns available: {names}")
    col = _get_column(table)
    operator = input("On what operator [=, !=, <, >, IN]: ")
    value = _get_value(table, col, operator)
    return [{"column": col, "operator": operator, "value": value}]


def _get_column(table: type[DB]) -> str:
    columns = list(table.get_class_fields(table))

    print("Select a column from the following:")
    for i, field in enumerate(columns):
        print(f"[{i + 1}] {field.name} ({field.type.__name__})")

    while True:
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(columns):
                return columns[choice - 1].name
            else:
                print("Invalid option.")
        except ValueError:
            print("Invalid type.")


def _get_value(table: type[DB], column: str, operator: str = None):
    field_type = table.get_class_field_type(table, column)
    value = input(f"{column} ({field_type}) {operator} ")
    try:
        return field_type(value)
    except (ValueError, TypeError):
        print("Invalid type.")
        return None


def search_values(table: type[DB]) -> None:
    conditions = _get_conditions(table)
    dict_to_table(table.find(conditions))


def add_values(table: type[DB]) -> None:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    names = ", ".join(names)

    print(f"Columns: {names}")
    values = input(
        f"Enter the entry you would like to add with values separated by commas: "
    )
    values = [v.strip() for v in values.split(",")]
    table(*values).insert()
    print("> Successfully added entry")
    sleep(0.8)


def update_values(table: type[DB]) -> None:
    while True:
        to_filter = (
            input(f"Do you want apply a filter to update? (Y/N): ").strip().upper()
        )
        if to_filter == "Y":
            conditions = _get_conditions(table)
            break
        if to_filter == "N":
            break
        else:
            continue

    col = _get_column(table)
    value = input("What is the new value? : ")
    rows = table.update({col: value}, conditions if conditions else None)
    print(f"Number of rows updated: {rows}")
    sleep(0.8)


def delete_values(table: type[DB]) -> None:
    while True:
        to_filter = (
            input(f"Do you want apply a filter to delete? (Y/N): ").strip().upper()
        )

        if to_filter == "Y":
            conditions = _get_conditions(table)
            rows = table.delete(conditions)
            print(f"Number of rows deleted {rows}.")
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
                table.delete()
                sleep(0.8)
                break
            else:
                continue


if __name__ == "__main__":
    from app.models.load import initiate, Aircrafts

    initiate()
    _get_value(Aircrafts, "age")

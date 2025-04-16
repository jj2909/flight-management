from app.tui.utils import dict_to_table
from app.models.base_model import DB


def _get_conditions(table: type[DB]) -> list[dict]:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    print(f"Columns available: {names}")
    col = input("What column do you want to filter by?: ")
    operator = input("On what operator [=, !=, <, >, IN]: ")
    print(f"{col} {operator} ?")
    value = input("What value?: ")
    return [{"column": col, "operator": operator, "value": value}]


def _get_column(table: type[DB]) -> str:
    columns = list(table.get_class_fields(table))

    print("Select a column from the following:")
    [print(f"[{i + 1}] {j.name} ({j.type.__name__})") for i, j in enumerate(columns)]

    while True:
        choice = input(">").strip()
        if choice.isdigit():
            if 0 <= (int(choice) - 1) < len(columns):
                return columns[int(choice) - 1].name

        print("Invalid option.")

def _get_value(table: type[DB], column: str, operator: str = None):
    x = input(f"{column} ")


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

    col = input("What column do you want to update? : ")
    value = input("What is the new value? : ")
    rows = table.update({col: value}, conditions if conditions else None)
    print(f"Number of rows updated: {rows}")


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
                break
            else:
                continue

if __name__=="__main__":
    from app.models.load import initiate, Aircrafts
    initiate()
    _get_value(Aircrafts)

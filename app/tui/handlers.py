from time import sleep
from app.base.exceptions import DuplicatePrimaryKeyError, ForeignKeyConstraintError
from app.tui.utils import dict_to_table
from app.models.base_model import DB


def _get_conditions(table: type[DB]) -> list[dict]:
    conditions = []
    while True:
        col = _get_column(table, "FILTER")
        operator = _get_operator()
        value = _get_value(table, col, operator)
        conditions.append({"column": col, "operator": operator, "value": value})
        if input("> Add another filter? [y]/[n]: ") != "y":
            break

    return conditions


def _get_column(table: type[DB], condition: str) -> str:
    columns = list(table.get_class_fields(table))

    print(f"\nSelect a column to {condition}: ")
    for i, field in enumerate(columns):
        print(f"[{i + 1}] {field.name} ({field.type.__name__})")

    while True:
        try:
            choice = int(input("> ").strip())
            if 1 <= choice <= len(columns):
                return columns[choice - 1].name
            else:
                print("ERROR: Invalid option")
        except ValueError:
            print("ERROR: Invalid option")


def _get_value(table: type[DB], column: str, operator: str = None):
    field_type = table.get_class_field_type(table, column)
    value = input(f"> {column} ({field_type.__name__}) {operator} ")
    while True:
        try:
            return field_type(value)
        except (ValueError, TypeError):
            print("ERROR: Invalid type")


def _get_operator() -> str:
    operators = ["=", "!=", "<", ">", "IN"]

    print("\nSelect an operator: ")
    for i, op in enumerate(operators):
        print(f"[{i + 1}] {op}")

    while True:
        try:
            choice = int(input("> ").strip())
            if 1 <= choice <= len(operators):
                return operators[choice - 1]
            else:
                print("ERROR: Invalid option")
        except ValueError:
            print("ERROR: Invalid option")


def search_values(table: type[DB]) -> None:
    conditions = _get_conditions(table)
    dict_to_table(table.find(conditions))


def add_values(table: type[DB]) -> None:
    fields = table.get_class_fields(table)
    names = [field.name for field in fields]
    names = ", ".join(names)

    while True:
        print(f"\nColumns: {', '.join(names)}")
        values = input(f"> Enter the record with values separated by commas: ")
        values = [v.strip() for v in values.split(",")]

        if len(values) != len(fields):
            print(f"ERROR: need {len(fields)} values, got {len(values)}")
            continue

        try:
            table(*values).insert()
            print("Successfully added record")
            sleep(0.8)
            break
        except ForeignKeyConstraintError:
            fk = table.get_foreign_keys(table)
            fk = [f"{key['to_table']}({key['to_column']})" for key in fk]
            print("\nERROR: Failed to add due to related records not existing")
            print(f"ERROR: Make sure your values exist in {', '.join(set(fk))}")
            print("ERROR: Or turn off foreign key restrictions in Settings")
            break
        except DuplicatePrimaryKeyError:
            print(f"\nERROR:{table.primary_key} already in use.")
            break
        except Exception as e:
            print(f"\nERROR: Values not added - unexpected error: {e}")
            break


def update_values(table: type[DB]) -> None:
    conditions = []
    if (input(f"\n> Apply a filter to update? [y]/[n]: ").strip().lower()) == "y":
        conditions = _get_conditions(table)
        print("Filter applied")
    else:
        print("No filter applied")

    col = _get_column(table, "UPDATE")
    print("What is the new value?")
    value = input(f"> {col} = ")

    while True:
        try:
            rows = table.update({col: value}, conditions)
            print(f"Number of rows updated: {rows}")
            sleep(0.8)
            break
        except ForeignKeyConstraintError:
            fk = table.get_foreign_keys(table)
            fk = [f"{key['to_table']}({key['to_column']})" for key in fk]
            print("\nERROR: Failed to add due to related records not existing")
            print(f"ERROR: Make sure your values exist in {', '.join(set(fk))}")
            print("ERROR: Or turn off foreign key restrictions in Settings")
            break
        except DuplicatePrimaryKeyError:
            print(f"\nERROR: {table.primary_key} already in use.")
            break
        except Exception as e:
            print(f"\nERROR: Values not added - unexpected error: {e}")
            break


def delete_values(table: type[DB]) -> None:
    while True:
        to_filter = input(f"> Apply a filter to delete? [y]/[n]: ").strip().lower()

        if to_filter == "y":
            conditions = _get_conditions(table)
            try:
                rows = table.delete(conditions)
                print(f"Number of rows deleted {rows}")
                sleep(0.8)
                break
            except ForeignKeyConstraintError:
                fk = table.get_foreign_keys(table)
                fk = [f"{key['to_table']}({key['to_column']})" for key in fk]
                print(
                    "\nERROR: Failed to delete record(s) due to existing related data"
                )
                print(
                    f"ERROR: Make sure your values do not exist in {", ".join(set(fk))}"
                )
                print("ERROR: or turn off foreign key restrictions in Settings")
                break
            except Exception as e:
                print(f"ERROR: Values not deleted - unexpected error: {e}")

        elif to_filter == "n":
            if (
                input(f"> Delete all records in {table.__name__}? [y]/[n]: ").lower()
            ) == "y":
                try:
                    table.delete()
                    print(f"All records from {table.__name__} deleted")
                    sleep(0.8)
                except Exception as e:
                    print(f"ERROR: Values not deleted - unexpected error: {e}")
                break
        else:
            print("ERROR: invalid option")


if __name__ == "__main__":
    from app.models.load import initiate, Aircrafts

    initiate()
    _get_value(Aircrafts, "age")

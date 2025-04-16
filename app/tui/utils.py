from tabulate import tabulate
from time import sleep

def dict_to_table(d: dict) -> None:
    if d:
        header = d[0].keys()
        rows = [x.values() for x in d]
        print(tabulate(rows, header))
        sleep(0.3)
    else:
        print("> Empty query")
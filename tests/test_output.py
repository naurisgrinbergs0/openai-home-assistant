import pandas as pd

file_name = "./tests/test.xlsx"
tables = {}


def table_create(table_name, column_names):
    tables[table_name] = {"columns": column_names, "data": [], "current_row": 0}


def table_append_value(table_name, value):
    if table_name not in tables:
        raise ValueError("No such table exists")
    if len(tables[table_name]["data"]) <= tables[table_name]["current_row"]:
        tables[table_name]["data"].append([])

    tables[table_name]["data"][tables[table_name]["current_row"]].append(value)


def table_next_row(table_name):
    if table_name not in tables:
        raise ValueError("No such table exists")
    tables[table_name]["current_row"] += 1


def table_export(table_name):
    if table_name not in tables:
        raise ValueError("No such table exists")

    columns = tables[table_name]["columns"]
    data = tables[table_name]["data"]
    df = pd.DataFrame(data, columns=columns)
    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer, sheet_name=table_name, index=False)

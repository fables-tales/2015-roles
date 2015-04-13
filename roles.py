import csv
from collections import defaultdict

def should_ignore_cell(ignore_rows, ignore_columns, row_idx, col_idx, cell_value):
    return any([
        row_idx in ignore_rows,
        col_idx in ignore_columns,
        cell_value.strip() == "",
        "static" in cell_value.lower(),
        "nobody" in cell_value.lower(),
    ])

def normalize_name(name):
    name = name.lower().replace("justin", "justyn").strip().split(" ")
    if len(name) > 1 and not "-" in name[-1]:
        name[-1] = name[-1][0]
    return " ".join(name)

def unique_names(cells):
    ignore_rows = [0]
    ignore_cols = [0]

    names = set()

    for row_idx, row in enumerate(cells):
        for col_idx, cell_value in enumerate(row):
            if not should_ignore_cell(ignore_rows, ignore_cols, row_idx, col_idx, cell_value):
                name = normalize_name(cell_value)
                names.add(name)

    return names


if __name__ == "__main__":
    r = csv.reader(open("data/roles.csv"))
    cells = list(r)
    people = sorted(unique_names(cells))

    roles = defaultdict(list)
    for row_idx, row in enumerate(cells[1:]):
        for col_idx, cell_value in enumerate(row[1:]):
            time = cells[0][col_idx+1]
            if time != "":
                role = cells[row_idx+1][0]
                if role != "":
                    roles[normalize_name(cell_value)].append((col_idx, time, role))


    for person in roles:
        with open("schedules/" + person.replace(" ", "_") + ".md", "w") as fp:
            fp.write("#SR2015 Schedule for " + person + "\n\n")
            fp.write("| time | role |\n")
            fp.write("|----|----|\n")
            for idx,time,role in sorted(roles[person], key=lambda x: x[0]):
                fp.write("| " + time + " | " + role + " |\n")

table = [
    ["1:00", 33, 34, "BUY"],
    ["1:01", 35, 36, "BUY"],
    ["1:02", 34, 35, "BUY"],
    ["1:03", 35, 33, "SELL"]
]

def get_subtables(table, action):
    subtables = []
    for i, row in enumerate(table):
        print(row[3])
        if row[3] == action:
            subtable = table[i:i + 3]
            if len(subtable) == 3:
                subtables.append(subtable)
    return subtables

action = "BUY"
subtables = get_subtables(table, action)

for i, subtable in enumerate(subtables):
    print(f"Instance {i + 1}:")
    for row in subtable:
        print(row)
    print()

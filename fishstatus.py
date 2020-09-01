def Status(name, data, badge_names):
    output = f" --- {name} the angler --- \n"

    output += f"Inventory:\n"

    if "bike" in data[name]["flags"]:
        output += " - A bicycle\n"

    for a in badge_names:
        if a in data[name]["flags"]:
            output += f" - [{a}] badge\n"

    for a in data[name]["flags"].keys():
        if "I :heart: " in a or "Visited " in a or "Go Team!" in a:
            output += f" - [{a}] badge\n"

    output += " - Bait box: "
    for a in data[name]["baitbox"].keys():
        output += f"[{data[name]['baitbox'][a]}] "

    output += "\n"

    output += f"Fish caught:\n"

    total_fish = 0
    for a in data[name]["catchlog"].keys():
        output += f" - {a} ({data[name]['catchlog'][a]})\n"
        total_fish += data[name]['catchlog'][a]

    output += f"Total: {total_fish} fish"
    return output
def Status(name, data, herbs, spices, badge_names, hide_badges=False, hide_fish=False):
    output = f" --- {name} the angler --- \n"

    output += f"Inventory:\n"

    if "bike" in data[name]["flags"]:
        output += " - A bicycle\n"
    if "surfboard" in data[name]["flags"]:
        output += " - A surfboard\n"
    if "crampons" in data[name]["flags"]:
        output += " - Crampons\n"
    if "platinumkey" in data[name]["flags"]:
        output += " - A Platinum Key\n"
    herbList = ""
    for a in herbs:
        if a in data[name]["flags"]:
            if herbList == "":
                herbList = a
            else:
                herbList = f"{herbList}, {a}"
    spiceList = ""
    for a in spices:
        if a in data[name]["flags"]:
            if spiceList == "":
                spiceList = a
            else:
                spiceList = f"{spiceList}, {a}"

    if herbList != "":
        output += f" - Herbs: {herbList}\n"

    if spiceList != "":
        output += f" - Spices: {spiceList}\n"


    badge_output = ""
    badge_count=0;
    for a in badge_names:
        if a in data[name]["flags"]:
            badge_output += f" - [{a}] badge\n"
            badge_count+=1

    for a in data[name]["flags"].keys():
        if "I :heart: " in a or "Visited " in a or "Go Team!" in a:
            badge_output += f" - [{a}] badge\n"
            badge_count+=1

    if hide_badges == False:
        output += badge_output
    

    output += " - Bait box: "
    for a in data[name]["baitbox"].keys():
        output += f"[{data[name]['baitbox'][a]}] "

    output += "\n"

    if hide_badges == True:
        output += f" {badge_count} Badges\n"

    fish_output = f"Fish caught:\n"

    total_fish = 0
    for a in data[name]["catchlog"].keys():
        fish_output += f" - {a} ({data[name]['catchlog'][a]})\n"
        total_fish += data[name]['catchlog'][a]
    
    fish_output += f"Total: {total_fish} Fish"

    if hide_fish == False:
        output+=fish_output
    else:
        output+=f" {total_fish} Fish\n"
        output+="Full inventory: "

    return output
from sosfish_constants import badge_names 
from sosfish_constants import other_badge_names
from sosfish_constants import herbs
from sosfish_constants import spices
from sosfish_constants import PokemonURL

def Status(name, data, compress_badges=False, hide_badges=False, hide_fish=False):
    output = f" --- {name} the angler --- \n"

    if len(data[name]["equipped"])>0:
        output += f"Wearing:\n"
        for a in data[name]["equipped"].keys():
            output += f" - {a}\n"

    output += f"Inventory:\n"

    if "bike" in data[name]["flags"]:
        output += " - A bicycle\n"
    if "surfboard" in data[name]["flags"]:
        output += " - A surfboard\n"
    if "crampons" in data[name]["flags"]:
        output += " - Crampons\n"
    if "platinumkey" in data[name]["flags"]:
        output += " - A platinum key\n"
    if "log" in data[name]["flags"]:
        output += " - A log\n"
    if "flintsteel" in data[name]["flags"]:
        output += " - A flint and steel\n"
    
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

    output += " - Bait box: "
    for a in data[name]["baitbox"].keys():
        output += f"[{data[name]['baitbox'][a]}] "
    output += "\n"

    badge_output = ""
    badge_count=0;

    if compress_badges:
        badge_output = " - Badges:\n"

    row_count=0
    for a in badge_names:
        if a in data[name]["flags"]:
            if compress_badges:
                badge_output += f"  [{a}]"
                row_count+=1
                if row_count>2:
                    badge_output +="\n"
                    row_count=0;
            else:
                badge_output += f" - [{a}] badge\n"

            badge_count+=1

    for a in other_badge_names:
        if a in data[name]["flags"]:
            if compress_badges:
                badge_output += f"  [{a}]"
                row_count+=1
                if row_count>2:
                    badge_output +="\n"
                    row_count=0;
            else:
                badge_output += f" - [{a}] badge\n"

            badge_count+=1


    for a in data[name]["flags"].keys():
        if "I :heart: " in a or "Visited " in a:
            if compress_badges:
                badge_output += f"  [{a}]"
                row_count+=1
                if row_count>2:
                    badge_output +="\n"
                    row_count=0;
            else:
                badge_output += f" - [{a}] badge\n"
            badge_count+=1

    if compress_badges:
        badge_output += "\n"
    
    if hide_badges == False:
        output += badge_output
    

    if hide_badges == True:
        output += f" {badge_count} Badges\n"

    fish_output = f"Catches:\n   "

    total_fish = 0
    for a in data[name]["catchlog"].keys():
        fish_output += f"{a} ({data[name]['catchlog'][a]}) "
        total_fish += data[name]['catchlog'][a]
        if (total_fish % 3) == 2:
        	fish_output += "\n   "
        else:
        	fish_output += ", "
    
    fish_output += f"\nTotal: {total_fish} Catches\n"

    if hide_fish == False:
        output+=fish_output
    else:
        output+=f" {total_fish} Catches\n"
    
    if data[name]["currentcompanion"]!="":
        output+= f"Current companion: {data[name]['currentcompanion']}\n"
        output+= PokemonURL(data[name]['currentcompanion'])
        output+="\n"
    if len(data[name]["companions"])>1:
        output+="Other friends: "
        for poke in data[name]["companions"]:
            output += f"[{poke}] "
        output+="\n"

    if hide_fish or hide_badges:
        output+="Full inventory: "



    return output
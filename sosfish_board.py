import re
import datetime
import sosfish_constants
from sosfish_constants import badge_text

def CheckLeaderBoard(data, user):
	most_fish_user=""
	most_fish_score=0

	most_fishtypes_user=""
	most_fishtypes_score=0

	most_badges_user=""
	most_badges_score=0

	for name in data.keys():
		#print(name)

		count_fish = 0
		for c in data[name]["catchlog"].keys():
			count_fish+=data[name]["catchlog"][c]

		if count_fish>most_fish_score:
			most_fish_user = name
			most_fish_score = count_fish

		if len(data[name]["catchlog"].keys())>most_fishtypes_score:
			most_fishtypes_score = len(data[name]["catchlog"].keys())
			most_fishtypes_user = name

		badges = 0
		for a in sosfish_constants.badge_names:
			if a in data[name]["flags"]:
				badges += 1
		for a in sosfish_constants.other_badge_names:
			if a in data[name]["flags"]:
				badges += 1
		for a in data[name]["flags"].keys():
			if "I :heart: " in a or "Visited " in a:
				badges += 1

		if badges>most_badges_score:
			most_badges_score = badges
			most_badges_user = name

	total_badges = len(data.keys())*2 + len(sosfish_constants.badge_names) + len(sosfish_constants.other_badge_names)
	total_fish_types = len(data.keys())*5

	output = f"Most Badges: {most_badges_user} ({most_badges_score}/{total_badges})"
	output += f"\nMost Fish: {most_fish_user} ({most_fish_score})"
	output += f"\nMost kinds of Fish: {most_fishtypes_user} ({most_fishtypes_score}/{total_fish_types})"

	if most_badges_user == user and "Achievement Get!" not in data[user]["flags"]:
		data[user]["flags"]["Achievement Get!"] = True
		output += f"\n{badge_text}[Achievement Get!]"
	if most_fish_user == user and "Relentless" not in data[user]["flags"]:
		data[user]["flags"]["Relentless"] = True
		output += f"\n{badge_text}[Relentless]"
	if user == most_fishtypes_user and "Master Explorer" not in data[user]["flags"]:
		data[user]["flags"]["Master Explorer"] = True
		output += f"\n{badge_text}[Master Explorer]"

	return output





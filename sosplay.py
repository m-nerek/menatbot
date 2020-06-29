# pip install youtube-search
from youtube_search import YoutubeSearch

def respond(message):

	searchTerm = str(message.content).lower().split("play",1)[1].strip()

	#if "CFTony" in message.author.name:
	#	searchTerm="rickroll"

	for i in range(5):
		results = YoutubeSearch(searchTerm, max_results=1)
		if len(results.videos)>0:
			return "https://www.youtube.com"+results.videos[0].get("link")
	return ":guile: I can't play that Tony"


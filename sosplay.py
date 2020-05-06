# pip install youtube-search
from youtube_search import YoutubeSearch

def respond(message):

	searchTerm = str(message).lower().split("play",1)[1].strip()

	
	results = YoutubeSearch(searchTerm, max_results=1)
	return "https://www.youtube.com"+results.videos[0].get("link")


print(respond("@menato play despacito"))
import json
cards = {}
with open("cards.json", "rb") as f:
	cards = json.loads(f.read())
	f.close()
	
settings = {}
with open("settings.json", "rb") as f:
	settings = json.loads(f.read())
	f.close()
if __name__ == "__main__":
	print(settings.keys())
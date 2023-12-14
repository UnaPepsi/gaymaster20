import requests,os

def rat(randNum: int,randIndex: int) -> str:
	link = requests.get(f"https://www.googleapis.com/customsearch/v1?key={os.environ['GOOGLE']}&q=rat animal&searchType=image&highRange={randNum}").json()
	image = link['items'][randIndex]['link']
	return image
from requests import get

def rand_copy_pasta():
	try:
		randpost = get("https://www.reddit.com/r/copypasta/random.json").json()
	except KeyError:
		return "Reddit's api is the most dogshit api that has ever existed and has the worst rate limit ever, so you have to wait to use this command again"
	return randpost[0]['data']['children'][0]['data']['selftext']
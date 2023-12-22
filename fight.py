import json,random

async def start_duel(player_1: str, player_2: str):
	with open("files/messages.json","r") as f:
		data = json.load(f)
	rand = random.randint(0,1)
	if rand == 1:
		victim = player_1
		attacker = player_2
	else:
		victim = player_2
		attacker = player_1
	return {
		"item":[random.choice(data['item']).format(player=player_1),random.choice(data['item']).format(player=player_1)],
		"prepare":[random.choice(data['prepare']).format(player=player_1),random.choice(data['prepare']).format(player=player_2)],
		"confrontation":[random.choice(data['confrontation']).format(victim=player_1,attacker=player_2),random.choice(data['confrontation']).format(victim=player_2,attacker=player_1)],
		"death":[random.choice(data['death']).format(victim=victim,attacker=attacker),attacker]
	}

# print(random.choice(data['item']).format(player=player_1))
# print(random.choice(data['item']).format(player=player_2))

# print(random.choice(data['prepare']).format(player=player_1))
# print(random.choice(data['prepare']).format(player=player_2))

# print(random.choice(data['confrontation']).format(victim=player_1,attacker=player_2))
# print(random.choice(data['confrontation']).format(victim=player_2,attacker=player_1))

# print(random.choice(data['death']).format(victim=victim,attacker=attacker))
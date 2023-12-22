import discord,os,fortnite,typing,oss,time,botchangelog,randompass,illumes,nitrogen,fight
from random import randint,choice
from asyncio import sleep
from requests import get
from keep_alive import keep_alive
from bs4 import BeautifulSoup
from discord.ext import commands, tasks

status = {"pepsi":"https://www.youtube.com/watch?v=nEHQiHGYZ0s",
					"tokaua":"https://www.youtube.com/watch?v=URBpbhH580k",
					"donovan":"https://www.youtube.com/watch?v=zdDeokVmgCE"}

def run_discord_bot():
	client = commands.Bot(command_prefix="",intents=discord.Intents.all())
	
	@client.event
	async def on_ready():
		print(f"{client.user} is now running")
		# await client.tree.sync()
		change_status.start()
		send_qotd.start()
	
	@client.event
	async def on_message(message: discord.Message):
		if message.author == client.user:
			return
		user_message = str(message.content).lower()
		# if user_message.split()[0] == "jajaxd" and message.author.id == 624277615951216643:
		# 	channel = client.get_guild(830871521080901743).get_channel(1186453245456031764)
		# 	await channel.send(message.content.split(maxsplit=1)[1])
		if user_message == "ratio":
			await message.add_reaction("\U0001F44D")
			await message.add_reaction("\U0001F44E")
		if user_message == "botsync":
			if message.author == client.get_user(624277615951216643):
				await message.add_reaction("\U0001F44D")
				print("synced")
				await client.tree.sync()

	@tasks.loop(seconds=20)
	async def change_status():
		name = choice(list(status))
		# await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{name}'s videos"),status=discord.Status.idle)
		await client.change_presence(activity = discord.Streaming(name=f"{name}'s videos",url=status[name]))
	@tasks.loop(minutes=10)
	async def send_qotd():
		sent_channel = await client.get_channel(1186453245456031764).fetch_message(1186705930428108983)
		qotd = sent_channel.content
		# print(qotd)
		if int(time.strftime("%H",time.localtime())) == 16 and qotd != "QOTD sent":
			channel = client.get_guild(607689950275698720).get_channel(1029245905204957215)
			await channel.send(f"QOTD:\n{qotd}")
			await sent_channel.edit(content="QOTD sent")

	@client.tree.command(description="Gets someone's BattlePass level")
	async def level(interaction: discord.Interaction,username: str):
		await interaction.response.send_message(fortnite.get_bp_level(username))
	@client.tree.command(description="Gets someone's BattlePass level")
	async def stats(interaction: discord.Interaction,
				 username: str, time_window: typing.Literal['lifetime','season'],
				 stat: typing.Literal["score", "scoreperwin", "scorepermatch", "wins", "top3", "top5", "top6", "top10", "top12", "top25", "kills", "killspermin", "killspermatch", "deaths", "kd", "matches", "winrate", "minutesplayed", "playersoutlived"],
				 mode: typing.Literal["overall", "solo", "duo", "squad", "ltm"]):
		await interaction.response.send_message(fortnite.get_stats(username,time_window,stat,mode))
	#Misc
	@client.tree.command(description="Shows how many days have passed since HolyPvP died.")
	async def holydied(interaction: discord.Interaction):
		await interaction.response.send_message(f"A total of {int((time.time()-1696791600)/86400)} days have passed since HolyPvP died")
	@client.tree.command(description="Shows how many days have passed since ViperMC died")
	async def viperdied(interaction: discord.Interaction):
		await interaction.response.send_message(f"A total of {int((time.time()-1701297218)/86400)} days have passed since ViperMC died")
	@client.tree.command(description="Is it Christmas?")
	async def isitchristmas(interaction: discord.Interaction):
		if time.localtime()[1] == 12 and time.localtime()[2] == 25:
			await interaction.response.send_message("Yes! Merry Christmas! :tada:")
		else:
			await interaction.response.send_message("No")
	@client.tree.command(description="GEOMETRY DASH")
	async def gd(interaction: discord.Interaction):
		await interaction.response.send_message("https://streamable.com/8kgjto GEOMETRY DASH BEOMMM")
	@client.tree.command(description="Chamoy")
	async def chamoy(interaction: discord.Interaction):
		await interaction.response.send_message("https://streamable.com/kzrd5r")
	
	#Osu!
	@client.tree.command(description="Shows you a list of someone's previous osu! names")
	async def pastnames(interaction: discord.Interaction, username: str):
		try:
			a = f"{username}'s previous usernames:"
			for i in oss.get_previous_username(username):
				a += f"\n{i}"
			await interaction.response.send_message(a)
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows the country of an osu! user")
	async def country(interaction: discord.Interaction, username: str):
		try:
			await interaction.response.send_message(f"{username} is registered on {oss.get_country(username)}")
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! supporter details")
	async def supporter(interaction: discord.Interaction, username: str):
		try:
			if oss.is_supporter(username):
				await interaction.response.send_message(f"{username} has supporter")
			else:
				if oss.has_supported(username):
					await interaction.response.send_message(f"{username} does not have supporter but has supported at least once")
				else:
					await interaction.response.send_message(f"{username} does not have supporter")
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! profile picture")
	async def pfp(interaction: discord.Interaction, username: str):
		try:
			await interaction.response.send_message(oss.pfp(username))
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! rank")
	async def rank(interaction: discord.Interaction, username: str):
		try:
			global_rank = oss.rank(username)[0]
			country_rank = oss.rank(username)[1]
			await interaction.response.send_message(f"Global rank: {global_rank}\nCountry rank: {country_rank}")
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's highest osu! rank")
	async def highestrank(interaction: discord.Interaction, username: str):
		try:
			await interaction.response.send_message(f"{username}'s highest rank: {oss.highest_rank(username)[0]}\nRecorded on: {oss.highest_rank(username)[1]}")
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows someone's osu! accuracy")
	async def acc(interaction: discord.Interaction, username: str):
		try:
			await interaction.response.send_message(f"{username}'s accuracy: {oss.acc(username)}")
		except ValueError:
			await interaction.response.send_message(f"Username {username} not found")
	@client.tree.command(description="Shows a random unsecured camera")
	async def randomcam(interaction: discord.Interaction):
		await interaction.response.defer()
		randNum= randint(1,99999)
		find=[]
		while True:
			image_link = f"http://images.opentopia.com/cams/{randNum}/big.jpg"
			code = get(image_link).status_code
			# print(code)
			if code == 200:
				link = get(f"http://www.opentopia.com/webcam/{randNum}")
				soup = BeautifulSoup(link.text,'html.parser')
				find = [soup.find("label",attrs={"class":"right country-name"}).text]
				try:
					find.append(soup.find("label",attrs={"class":"right region"}).text)
				except AttributeError:
					find.append("Not Found")
				try:
					find.append(soup.find("span",attrs={"class":"latitude"}).text)
					find.append(soup.find("span",attrs={"class":"longitude"}).text)
				except AttributeError:
					find.append("Not")
					find.append("Found")
				break
			randNum= randint(1,99999)
		await interaction.followup.send(f"Country: {find[0]}, State/Region: {find[1]}, Coordinates: {find[2]}, {find[3]}\n{image_link}")
	@client.tree.command(description="Is GeometryDash 2.2 out?")
	async def isgdout(interaction: discord.Interaction):
		value = get("https://api.steamcmd.net/v1/info/322170").json()
		if value['data']['322170']['depots']['branches']['public']['timeupdated'] == "1511222225":
			await interaction.response.send_message("No")
		else:
			await interaction.response.send_message("Yes, finally!!!")
	@client.tree.command(description="Sends the Rats Invaders .apk")
	async def ratsapk(interaction: discord.Interaction):
		await interaction.response.defer()
		await interaction.followup.send(file=discord.File("files/ratsinvaders2.0.apk"))
	@client.tree.command(description="Annonymously DMs someone")
	async def dm(interaction: discord.Interaction, user: discord.User, message: str):
		try:
			await discord.DMChannel.send(user,f"You have received an annonymous message!\n{message}")
			await interaction.response.send_message(f"Successfully DM'd {user} with message: {message}",ephemeral=True)
		except Exception:
			await interaction.response.send_message(f"Could not DM {user}, perhaps they have DMs disabled?",ephemeral=True)
	@client.tree.command(description="Send Pepsi a suggestion :)")
	async def suggest(interaction: discord.Interaction, suggestion: str):
		user = client.get_user(624277615951216643)
		dm_channel = await user.create_dm()
		await dm_channel.send(f"You have received a suggestion by {interaction.user.name}!\n{suggestion}")
		await interaction.response.send_message("Thank you for the suggestion :)")
	@client.tree.command(description="Shows someone's Fortnite stats in an image")
	async def imgstats(interaction: discord.Interaction, username: str, time_window: typing.Literal['lifetime','season']):
		await interaction.response.send_message(fortnite.img_stats(username,time_window))
	@client.tree.command(description="Generates a random passsowrd")
	async def randpass(interaction: discord.Interaction, lower: bool,upper: bool,
					numbers: bool,symbols: bool,length: int):
		print(f"{interaction.user.name} used randpass")
		await interaction.response.send_message(f"```{randompass.pass_gen(lower,upper,numbers,symbols,length)}```",ephemeral=True)
	@client.tree.command(description="Shows a random rat")
	async def rat(interaction: discord.Interaction):
		await interaction.response.send_message(illumes.rat(randint(0,10),randint(0,9)))
	@client.tree.command(description="Changes the QOTD")
	async def qotd(interaction: discord.Interaction, qotd: str):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("Pepsi command only")
		else:
			sent_channel = await client.get_channel(1186453245456031764).fetch_message(1186705930428108983)
			await sent_channel.edit(content=qotd)
			await interaction.response.send_message(f"Changed QOTD to {qotd}\nRemember to use this command past 10am")
	@client.tree.command(description="Shows the bot's changelog")
	async def changelog(interaction: discord.Interaction,version: str):
		await interaction.response.send_message(botchangelog.changelog(version))
	@client.tree.command(description="Uses stupid OperaGX nitro promotion exploit to generate nitro codes")
	async def getnitro(interaction: discord.Interaction):
		await interaction.response.send_message(f"https://discord.com/billing/partner-promotions/1180231712274387115/{nitrogen.nitro_gen()}")
	@client.tree.command(description="gen")
	async def pepsigen(interaction: discord.Interaction):
		if interaction.user.id != 624277615951216643:
			await interaction.response.send_message("Pepsi command only")
			return
		else:
			await interaction.response.defer()
			for i in range(50):
				user = client.get_user(624277615951216643)
				dm_channel = await user.create_dm()
				await dm_channel.send(f"<https://discord.com/billing/partner-promotions/1180231712274387115/{nitrogen.nitro_gen()}>")
		await interaction.followup.send("Done.")
	@client.tree.command(description="Duels someone!")
	async def duel(interaction: discord.Interaction, oponent: discord.User):
		if interaction.user.id == oponent.id:
			await interaction.response.send_message("You can't duel yourself!")
			return
		data = fight.start_duel(interaction.user.name,oponent.name)
		# print(data)
		channel = client.get_channel(interaction.channel_id)
		await interaction.response.send_message(f"Starting duel between <@{interaction.user.id}> and <@{oponent.id}>")
		await sleep(2)
		await channel.send(data['item'][0])
		await sleep(4)
		await channel.send(data['item'][1])
		await sleep(5)
		await channel.send(data['prepare'][0])
		await sleep(4)
		await channel.send(data['prepare'][1])
		await sleep(5)
		await channel.send(data['confrontation'][0])
		await sleep(4)
		await channel.send(data['confrontation'][1])
		await sleep(7)
		await channel.send(data['death'][0])
		await channel.send(f"{data['death'][1]} wins!")
	keep_alive()
	client.run(os.environ['TOKEN'])

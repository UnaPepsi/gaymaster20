import discord,os,fortnite,typing,oss,time,botchangelog
from random import randint
from requests import get
from keep_alive import keep_alive
from bs4 import BeautifulSoup
from discord.ext import commands



def run_discord_bot():
	client = commands.Bot(command_prefix="-",intents=discord.Intents.all())
	
	@client.event
	async def on_ready():
		print(f"{client.user} is now running")
		await client.tree.sync()

	@client.event
	async def on_message(message):
		if message.author == client.user:
			return

		user_message = str(message.content)
		if user_message.lower() == "ratio":
			await message.add_reaction("\U0001F44D")
			await message.add_reaction("\U0001F44E")

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
		if time.localtime()[1] == 11 and time.localtime()[2] == 25:
			await interaction.response.send_message("Yes! Merry Christmas! :tada:")
		else:
			await interaction.response.send_message("No")
	@client.tree.command(description="GEOMETRY DASH")
	async def gd(interaction: discord.Interaction):
		await interaction.response.send_message("https://streamable.com/m42w6m GEOMETRY DASH BEOMMM")
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
				find = [soup.find("label",attrs={"class":"right country-name"}).text,
							 soup.find("label",attrs={"class":"right region"}).text]
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
	@client.tree.command(description="Shows the bot's changelog")
	async def changelog(interaction: discord.Interaction):
		await interaction.response.send_message(botchangelog.changelog("2.6.0"))
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
	async def suggest(interaction: discord.Interaction, suggestion: str):
		await discord.DMChannel(id=624277615951216643,message=f"You have received a suggestion by {interaction.user.name}!\n{suggestion}")
	async def imgstats(interaction: discord.Interaction, username: str):
		await interaction.response.send_message(fortnite.img_stats(username))
	
	keep_alive()
	client.run(os.environ['TOKEN'])

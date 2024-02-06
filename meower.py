import subprocess
import time
from MeowerBot import Bot, CallBackIds
from MeowerBot.context import Context, Post, PartialUser, User
from MeowerBot.cog import Cog
from MeowerBot.command import command
import logging
from uwuify import YU, STUTTER, uwu
import requests

from dotenv import load_dotenv # type: ignore

load_dotenv() # type: ignore

from os import environ as env
from MeowerBot.ext.help import Help as HelpExt

logging.basicConfig(
	level=logging.DEBUG,
	handlers=[
		logging.FileHandler("debug.log", encoding='utf8'),
		logging.StreamHandler()
	]
)

logging.getLogger("websockets.client").setLevel(logging.INFO)
bot = Bot()

import os

@bot.event
async def login(_token):
	print("Logged in!")


@bot.command(name="ping")
async def ping(ctx: Context):
	await ctx.send_msg("Pong!\n My latency is: " + str(bot.latency))

# god is dead, and the below function is what killed it
@bot.command(name="uwuify")
async def uwuify(ctx: Context, *message: str):
	flags = YU | STUTTER
	new_message = str(uwu(' '.join(message), flags=flags))
	await ctx.send_msg(new_message)

@bot.command(name="googlecontinue")
async def googlesearchsuggestions(ctx: Context, *message: str):
	import requests
	from urllib.parse import quote
	from xml.etree import ElementTree

	search_term = ' '.join(message)
	url = f"https://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q={quote(search_term)}"
	response = requests.get(url)
	suggestions = ElementTree.fromstring(response.content)

	suggestions_list = [suggestion.attrib['data'] for suggestion in suggestions.iter('suggestion')]

	await ctx.send_msg("\n".join(suggestions_list))

@bot.command(name="24h")
async def twentyfour(ctx: Context):
	twenty_four_clock = time.strftime("%H:%M")

	await ctx.send_msg(f"Current time in 24h: {twenty_four_clock}")

@bot.command(name="timezone")
async def timezoneconverter(ctx: Context, *time: str, timezone: str = "utc", to_timezone: str = "utc"):
	from datetime import datetime

	time = ' '.join(time)
	
	from pytz import timezone
	from_zone = timezone(timezone)
	to_zone = timezone(to_timezone)
	utc_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
	from_zone.localize(utc_time).astimezone(to_zone)

# noinspection PyIncorrectDocstring
@bot.command(name="logs")
async def get_logs(ctx: Context, *args):
	"""
	Arguments:
		start: Optional[int]
		end: Optional[int]

	Formated like this:
		start=...

	@prefix get_logs start=-200 end=-1
	"""
	# start=...
	# end=...
	start = -10
	end = -1
	arg: str
	for arg in args:
		if arg.startswith("start"):
			start = int(arg.split("=")[1])
		elif arg.startswith("end"):
			end = int(arg.split("=")[1])

	with open("debug.log") as logfile:
		logs = logfile.readlines()

	message = await ctx.send_msg("".join(logs[start: end]))
	if not message:
		await ctx.reply("Error: Logs to big for current env")


@bot.command(name="bots")
async def get_bots(ctx: Context):
	await ctx.reply(f'\n {" ".join(list(bot.cache.bots.keys()))}')


@ping.subcommand(name="pong")
async def pong(ctx: Context):
	await ctx.send_msg("Pong!")

class Ping(Cog):
	def __init__(self, bot: Bot):
		super().__init__()
		self.bot = bot

	@command()
	async def cog_ping(self, ctx: Context):
		await ctx.send_msg("Pong!\n My latency is: " + str(self.bot.latency))
		print(bot.api.headers.get("token"))
	@cog_ping.subcommand()
	async def ping(self, ctx: Context):
		await ctx.send_msg("Pong!\n My latency is: " + str(self.bot.latency))

class Uwuify(Cog):
	def __init__(self, bot: Bot):
		super().__init__()
		self.bot = bot

	@command()
	async def cog_uwuify(self, ctx: Context, *message: str):
		flags = YU | STUTTER
		new_message = str(uwu(str(message), flags=flags))
		await ctx.send_msg(new_message)

class GoogleContiue(Cog):
	def __init__(self, bot: Bot):
		super().__init__()
		self.bot = bot

	@command()
	async def cog_googlecontinue(self, ctx: Context, *message: str):
		import requests
		from urllib.parse import quote
		from xml.etree import ElementTree

		search_term = ' '.join(message)
		url = f"https://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q={quote(search_term)}"
		response = requests.get(url)
		suggestions = ElementTree.fromstring(response.content)

		suggestions_list = [suggestion.attrib['data'] for suggestion in suggestions.iter('suggestion')]

		await ctx.send_msg("\n".join(suggestions_list))
		
class Gpt2(Cog):
	def __init__(self, bot: Bot):
		super().__init__()
		self.bot = bot

	@command()
	async def cog_gpt2(self, ctx: Context, *message: str):
		await ctx.send_msg("FOW SOME WEASON THIS SPECIFIC COG DOESN'T WOWK. >w< USE @Ultanium gpt2 INSTEAD")
		

async def welcome_post(ctx: Context):
	await ctx.send_msg("Uwtanyium Bot by DiffewentDance8 has nyow *whispers to self* been woaded?!!")

async def blaze(ctx: Context):
	await ctx.send_msg("Blaze >> Meower")

@bot.event
async def login(token):
	assert await bot.get_chat("9bf5bddd-cd1a-4c0d-a34c-31ae554ed4a7").fetch() is not None
	assert await bot.get_chat("9bf5bddd").fetch() is None
	assert await PartialUser(bot.user.username, bot).fetch() is not None
	assert await PartialUser("A" * 21, bot).fetch() is None
	welcome_post()

@bot.listen(CallBackIds.message)
async def on_message(message: Post):
	assert isinstance(message, Post)
	assert isinstance(bot.get_context(message), Context)



bot.register_cog(Ping(bot))
bot.register_cog(Uwuify(bot))
bot.register_cog(GoogleContiue(bot))
bot.register_cog(Gpt2(bot))
bot.register_cog(HelpExt(bot, disable_command_newlines=True))

@bot.command(name="maintenance")
async def post_and_leave(ctx: Context):
	# Add anti-bad measures
	if ctx.user.username == "DifferentDance8":
		# Post the message
		await ctx.send_msg("DiffewentDance8 is just *whispers to self* d-d-doing some m-maintenyance wowk on me, and as a w-wesuwt of that I wiww be offwinye fow a bit. *whispers to self* Don't wowwy, I'ww be back in a few minyutes.")
		# Wait 2 seconds
		time.sleep(5)
		exit()
	else:
		await ctx.send_msg("You do nyot have pewmission t-to inyitiate m-maintenyance.")

bot.run(env["ultusername"], env["ultpassword"])
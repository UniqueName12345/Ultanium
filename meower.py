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

import datetime
from dateutil import tz

@bot.command(name="convert_time")
async def convert_time(ctx: Context, time_str: str, from_tz_str: str, to_tz_str: str):
    try:
        from_tz = tz.gettz(from_tz_str)
        to_tz = tz.gettz(to_tz_str)

        # Parse the time string into a datetime object.
        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
        time_obj = time_obj.replace(tzinfo=from_tz)

        # Convert the time to the target timezone.
        converted_time = time_obj.astimezone(to_tz)

        await ctx.send_msg(f'The time {time_str} in {from_tz_str} is {converted_time.strftime("%H:%M")} in {to_tz_str}.')
    except OSError as e:
        print(f"An OSError occurred: {e}")

from transformers import GPT2LMHeadModel, GPT2Tokenizer

#Load pre-trained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

from collections import defaultdict

# Create a dictionary to keep track of the last time a user used the command
last_command_time = defaultdict(int)

import urllib.parse

@bot.command(name="continue")
async def continue_text(ctx: Context, *message: str):
    text = ' '.join(message)
    text = text.replace('@', 'AT')
    inputs = tokenizer.encode(text, return_tensors='pt')

    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, do_sample=True, temperature=0.7)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    await ctx.send_msg(generated_text)

import random

@bot.command(name="rps")
async def play_rps(ctx: Context, user_choice: str):
    """This function plays a game of rock-paper-scissors with the user"""
    bot_choices = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(bot_choices)

    if user_choice not in bot_choices:
        await ctx.send_msg("Invalid choice. Please choose rock, paper, or scissors.")
        return

    if user_choice == bot_choice:
        await ctx.send_msg(f"Draw! We both chose {bot_choice}.")
    elif (user_choice == 'rock' and bot_choice == 'scissors') or (user_choice == 'scissors' and bot_choice == 'paper') or (user_choice == 'paper' and bot_choice == 'rock'):
        await ctx.send_msg(f"You win! Your {user_choice} beats my {bot_choice}.")
    else:
        await ctx.send_msg(f"I win! My {bot_choice} beats your {user_choice}.")

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
		

@bot.event
async def login(token):
	assert await bot.get_chat("9bf5bddd-cd1a-4c0d-a34c-31ae554ed4a7").fetch() is not None
	assert await bot.get_chat("9bf5bddd").fetch() is None
	assert await PartialUser(bot.user.username, bot).fetch() is not None
	assert await PartialUser("A" * 21, bot).fetch() is None


@bot.listen(CallBackIds.message)
async def on_message(message: Post):
	assert isinstance(message, Post)
	assert isinstance(bot.get_context(message), Context)



bot.register_cog(Ping(bot))
bot.register_cog(Uwuify(bot))
bot.register_cog(GoogleContiue(bot))
bot.register_cog(Gpt2(bot))
bot.register_cog(HelpExt(bot, disable_command_newlines=True))

bot.run(env["ultusername"], env["ultpassword"])
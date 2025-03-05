# bot.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import environ
from database.db import init_db
from tasks.daily_reminder import DailyReminder

# Load environment variables
load_dotenv()

# Initialize the database
init_db()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Set up the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Load commands and events
async def load_extensions():
    await bot.load_extension("commands.hello")
    await bot.load_extension("commands.ping")
    await bot.load_extension("commands.forcesparkle")
    await bot.load_extension("commands.leaderboard")
    await bot.load_extension("commands.whoareyou")
    await bot.load_extension("events.on_message")  # Load the on_message event

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await load_extensions()
    DailyReminder(bot)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Run the bot
bot.run(environ.get('TOKEN'))

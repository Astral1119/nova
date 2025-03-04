# events/on_message.py
import random
import re
import discord
from database.db import update_sparkle

async def on_message(message: discord.Message):
    """
    Handles the on_message event for sparkle reactions and :boom: reactions.
    """
    # Ignore messages from the bot itself and other bots
    if message.author.bot:
        return

    # Check for "b" + 2 or more "o"s + "m" (case-insensitive)
    if re.search(r"\bb[o]{2,}m\b", message.content, re.IGNORECASE):
        await message.add_reaction("💥")  # :boom: emoji

    # Generate a random number between 1 and 100,000
    chance = random.randint(1, 100000)

    # Check for epic sparkle reaction (1/100,000 chance)
    if chance == 1:
        await message.add_reaction("✨")  # Epic sparkle
        await message.reply(f"**{message.author.name}** got an **epic sparkle**! ✨", mention_author=False)
        update_sparkle(message.author.id, "epic")

    # Check for rare sparkle reaction (1/10,000 chance)
    elif chance <= 10:
        await message.add_reaction("🌟")  # Rare sparkle
        await message.reply(f"**{message.author.name}** got a **rare sparkle**! 🌟", mention_author=False)
        update_sparkle(message.author.id, "rare")

    # Check for regular sparkle reaction (1/1,000 chance)
    elif chance <= 100:
        await message.add_reaction("⭐")  # Regular sparkle
        await message.reply(f"**{message.author.name}** got a **sparkle**! ⭐", mention_author=False)
        update_sparkle(message.author.id, "regular")

async def setup(bot):
    """
    Registers the on_message event with the bot.
    """
    bot.add_listener(on_message, "on_message")

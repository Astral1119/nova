# events/on_message.py
import random
import re
import discord

async def on_message(message: discord.Message):
    # Ignore messages from the bot itself and other bots
    if message.author.bot:
        return

    # Initialize server data if it doesn't exist
    server_id = str(message.guild.id)
    if server_id not in message.bot.sparkles:
        message.bot.sparkles[server_id] = {}
    if str(message.author.id) not in message.bot.sparkles[server_id]:
        message.bot.sparkles[server_id][str(message.author.id)] = {"epic": 0, "rare": 0, "regular": 0}

    # Check for "b" + 2 or more "o"s + "m" (case-insensitive)
    if re.search(r"\bb[o]{2,}m\b", message.content, re.IGNORECASE):
        await message.add_reaction("💥")  # :boom: emoji

    # Generate a random number between 1 and 100,000
    chance = random.randint(1, 100000)

    # Check for epic sparkle reaction (1/100,000 chance)
    if chance == 1:
        await message.add_reaction("✨")  # Epic sparkle
        await message.reply(f"**{message.author.name}** got an **epic sparkle**! ✨", mention_author=False)
        message.bot.sparkles[server_id][str(message.author.id)]["epic"] += 1
        message.bot.save_sparkles(message.bot.sparkles)  # Save the updated data

    # Check for rare sparkle reaction (1/10,000 chance)
    elif chance <= 10:
        await message.add_reaction("🌟")  # Rare sparkle
        await message.reply(f"**{message.author.name}** got a **rare sparkle**! 🌟", mention_author=False)
        message.bot.sparkles[server_id][str(message.author.id)]["rare"] += 1
        message.bot.save_sparkles(message.bot.sparkles)  # Save the updated data

    # Check for regular sparkle reaction (1/1,000 chance)
    elif chance <= 100:
        await message.add_reaction("⭐")  # Regular sparkle
        await message.reply(f"**{message.author.name}** got a **sparkle**! ⭐", mention_author=False)
        message.bot.sparkles[server_id][str(message.author.id)]["regular"] += 1
        message.bot.save_sparkles(message.bot.sparkles)  # Save the updated data

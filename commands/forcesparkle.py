# commands/forcesparkle.py
import discord
from discord.ext import commands

YOUR_USER_ID = 252130669919076352  # Your Discord user ID

class ForceSparkle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="forcesparkle", description="Force a sparkle reaction on a message (only for you)")
    async def forcesparkle(self, ctx: commands.Context, message_id: str, reaction_type: str):
        # Check if the user is Lilac
        if ctx.author.id != YOUR_USER_ID:
            await ctx.send("You don't have permission to use this command.", ephemeral=True)
            return

        # Validate reaction type
        valid_reactions = {
            "epic": "✨",
            "rare": "🌟",
            "regular": "⭐"
        }

        if reaction_type.lower() not in valid_reactions:
            await ctx.send("Invalid reaction type. Use `epic`, `rare`, or `regular`.", ephemeral=True)
            return

        # Fetch the message by ID
        try:
            message = await ctx.channel.fetch_message(int(message_id))
        except discord.NotFound:
            await ctx.send("Message not found. Make sure the message ID is correct and the message is in this channel.", ephemeral=True)
            return
        except discord.Forbidden:
            await ctx.send("I don't have permission to access that message.", ephemeral=True)
            return
        except ValueError:
            await ctx.send("Invalid message ID. Please provide a valid message ID.", ephemeral=True)
            return

        # Add the reaction
        emoji = valid_reactions[reaction_type.lower()]
        await message.add_reaction(emoji)
        await ctx.send(f"Added {emoji} reaction to the message!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ForceSparkle(bot))

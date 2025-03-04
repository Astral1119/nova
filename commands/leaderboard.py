# commands/leaderboard.py
import discord
from discord.ext import commands
from discord import app_commands
from database.db import get_leaderboard

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description="Show the sparkle leaderboard")
    @app_commands.describe(sparkle_type="The type of sparkle to show the leaderboard for")
    async def leaderboard(self, interaction: discord.Interaction, sparkle_type: str):
        """
        Displays the leaderboard for a specific sparkle type.
        """
        valid_types = ["epic", "rare", "regular"]
        if sparkle_type.lower() not in valid_types:
            await interaction.response.send_message(
                "Invalid sparkle type. Use `epic`, `rare`, or `regular`.",
                ephemeral=True
            )
            return

        leaderboard = get_leaderboard(sparkle_type.lower())
        if not leaderboard:
            await interaction.response.send_message(
                "No sparkles have been awarded yet.",
                ephemeral=True
            )
            return

        # Fetch user objects to get their usernames
        users = []
        for user_id, count in leaderboard:
            user = await self.bot.fetch_user(user_id)
            users.append(f"{user.name}: {count}")

        # Format the leaderboard
        leaderboard_text = "\n".join(users)
        await interaction.response.send_message(
            f"**{sparkle_type.capitalize()} Sparkle Leaderboard:**\n{leaderboard_text}",
            ephemeral=False  # Make the response visible to everyone
        )

    @leaderboard.autocomplete("sparkle_type")
    async def sparkle_type_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        """
        Provides autocomplete options for the sparkle_type argument.
        """
        valid_types = ["epic", "rare", "regular"]
        return [
            app_commands.Choice(name=sparkle_type, value=sparkle_type)
            for sparkle_type in valid_types
            if current.lower() in sparkle_type.lower()
        ]

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))

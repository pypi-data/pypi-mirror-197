"""Allow Sickw lookup from discord cog"""
import os
import discord
from discord import app_commands
from discord.ext import commands
from shiny_api.classes.sickw_results import SickwResult

print(f"Importing {os.path.basename(__file__)}...")


class SickwCog(commands.Cog):
    """Sickw functions"""

    def __init__(self, client: commands.Cog):
        self.client = client

    @app_commands.command(name="sick")
    @app_commands.checks.has_role("Shiny")
    async def sickw_lookup_command(self, context: discord.Interaction, serial_number: str):
        """Look up serial number in Sickw"""
        device = SickwResult(serial_number=serial_number)
        await context.response.send_message(device)


async def setup(client: commands.Cog):
    """Add cog"""
    await client.add_cog(SickwCog(client))

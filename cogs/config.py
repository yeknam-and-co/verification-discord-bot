import discord
from discord.ext import commands
from discord import app_commands
from helper.db import fetch_entire_guild

class config(commands.Cog):
    def __init__(self, bot): # steal bot from parent 
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self.qualified_name} is loaded.') #yay its loaded

    @app_commands.command(name="config", description="reports back the config")
    async def config(self, interaction: discord.Interaction):
        guild = fetch_entire_guild(interaction.guild.id)

        if guild is None:
            await interaction.response.send_message(f"no config found, run /setup to set up the bot", ephemeral=True)
            return

        verification_channel = interaction.guild.get_channel(guild[1])
        verification_role = interaction.guild.get_role(guild[2])
        staff_channel = interaction.guild.get_channel(guild[3])

        await interaction.response.send_message(f"channel: {verification_channel.mention} role: {verification_role.mention} staff channel: {staff_channel.mention}\nrerun /setup to change things", ephemeral=True)

async def setup(bot):
    await bot.add_cog(config(bot)) # add the cog to the bot

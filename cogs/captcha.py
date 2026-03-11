import discord
from discord.ext import commands
from discord import app_commands
from helper.captchasender import send_captcha
from discord.ui import Button, View

class captcha(commands.Cog):
    def __init__(self, bot): # steal bot from parent 
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self.qualified_name} is loaded.') #yay its loaded

    @app_commands.command(name="captcha", description="Generate a captcha")
    async def captcha(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="verification",
            description="click the button to verify your account.",
            color=discord.Color.blurple())

        button = Button(label="verify", style=discord.ButtonStyle.green)

        async def button_callback(interaction: discord.Interaction): # if the button is clicked, send the captcha
            await send_captcha(interaction, self.bot, interaction.user, interaction.user.id)

        button.callback = button_callback
        view = View(timeout=None)
        view.add_item(button)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(captcha(bot)) # add the cog to the bot

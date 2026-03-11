import discord
from discord.ui import Button, View
from helper.captchasender import send_captcha
from discord.ext import commands

async def verification_message(interaction: discord.Interaction, bot: commands.Bot, channel_id: int):
    print(channel_id)
    channel = interaction.guild.get_channel(channel_id)

    if channel is None:
        channel = await bot.fetch_channel(channel_id)

    print(channel)

    embed = discord.Embed(
        title="verification",
        description="click the button to verify your account.",
        color=discord.Color.blurple()
    )

    button = Button(label="verify", style=discord.ButtonStyle.green)

    async def button_callback(interaction: discord.Interaction):
        await send_captcha(interaction, bot, interaction.user, interaction.user.id)

    button.callback = button_callback

    view = View(timeout=None)
    view.add_item(button)

    await channel.send(embed=embed, view=view)
import discord
from discord.ext import commands
from helper.captchahelper import generate_captcha
import asyncio

async def send_captcha(interaction: discord.Interaction, bot: commands.Bot):
    def check(message):
        return message.author == interaction.user # check if the message is from the user

    captcha_text, image_path = generate_captcha()

    # create embed with image and send it to the user
    embed = discord.Embed(
    title="captcha",
    description="you have to solve the captcha to continue.",
    color=discord.Color.blurple())
    embed.set_image(url=f'attachment://{image_path}')

    await interaction.response.send_message(embed=embed, file=discord.File(image_path))

    try:
        response = await bot.wait_for('message', check=check, timeout=60) # wait for a message and check if it is from the user
        if response.content == captcha_text:
            await interaction.followup.send(f'{interaction.user.mention} has solved the captcha! {captcha_text}')
        else:
            await interaction.followup.send(f'{interaction.user.mention} has failed the captcha! {captcha_text}')
    except asyncio.TimeoutError:
        await interaction.followup.send(f'{interaction.user.mention} has failed the captcha! {captcha_text}')

import discord
from discord.ext import commands
from helper.captchahelper import generate_captcha
import asyncio
import os
from helper.db import fetch_guild_role
from helper.logger import log_action
async def send_captcha(interaction: discord.Interaction, bot: commands.Bot, user: discord.User, user_id: int):
    def check(message):
        return message.author == interaction.user # check if the message is from the user

    captcha_text, image_path = generate_captcha(user_id)

    # create embed with image and send it to the user
    embed = discord.Embed(
    title="captcha",
    description="you have to solve the captcha to continue.",
    color=discord.Color.blurple())
    embed.set_image(url=f'attachment://{image_path}')

    try:
        await user.send(embed=embed, file=discord.File(image_path))
    except discord.Forbidden:
        await interaction.followup.send(f'{interaction.user.mention} please enable DMs so i can message you!', ephemeral=True)
        await log_action(bot, "failed to send DM", user, interaction.guild.id)
        os.remove(image_path)
        return

    try:
        response = await bot.wait_for('message', check=check, timeout=60) # wait for a message and check if it is from the user
        if response.content == captcha_text:
            await user.send(f'you solved the captcha! you have been verified!')
            await log_action(bot, "solved the captcha", user, interaction.guild.id)

            role_id = fetch_guild_role(interaction.guild.id)
            role = interaction.guild.get_role(role_id)
            try:
                await user.add_roles(role)
            except discord.Forbidden:
                await log_action(bot, "no permission to add roles big alert", user, interaction.guild.id)
                await user.send(f'please contact a staff member to manually add the role')
            os.remove(image_path)
        else:
            await user.send(f'you failed the captcha! try again!')
            await log_action(bot, "failed the captcha", user, interaction.guild.id)
            os.remove(image_path)
    except asyncio.TimeoutError:
        await user.send(f'you failed the captcha! try again!')
        await log_action(bot, "timed out while solving the captcha", user, interaction.guild.id)
        os.remove(image_path)

    
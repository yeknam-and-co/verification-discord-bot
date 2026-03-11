from helper.db import fetch_guild_staff_channel
from datetime import datetime

async def log_action(bot, message, user, guild_id):

    channel_id = fetch_guild_staff_channel(guild_id)

    if channel_id is None:
        return

    channel = bot.get_channel(channel_id)
    if channel is None:
        channel = await bot.fetch_channel(channel_id)
    await channel.send(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {user.mention}: {message}')
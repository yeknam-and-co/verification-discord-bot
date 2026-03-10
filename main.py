import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.tree.sync()
    print("Commands synced!")

async def main(): # cogs
    async with bot:
        for i in os.listdir('cogs'):
            if i.endswith('.py'):
                await bot.load_extension(f'cogs.{i[:-3]}')
                print(f'Loaded cog {i[:-3]}')
            else:
                print(f'Skipped {i} because it does not end with .py')
                
        print("All cogs loaded!")
        await bot.start(TOKEN)

asyncio.run(main())

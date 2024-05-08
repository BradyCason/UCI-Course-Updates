import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

from bot_cog import Updates

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents=discord.Intents.all()
help_command = commands.DefaultHelpCommand(show_parameter_descriptions=False)
bot = commands.Bot(command_prefix='!', intents=intents, help_command=help_command)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{bot.user.name} has connected to Discord!')
    await bot.add_cog(Updates(bot, guild))

    channel = None
    for c in guild.channels:
        if c.name == "general" and isinstance(c, discord.TextChannel):
            channel = c
    if channel:
        await channel.send("UCI Course Notifications Bot is running. Check if the bot appears online to see if it is running.")

if __name__ == "__main__":
    bot.run(TOKEN)
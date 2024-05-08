# Initialize Discord bot to manage course subscriptions and notifications
# Copyright (C) 2024  Brady Cason

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
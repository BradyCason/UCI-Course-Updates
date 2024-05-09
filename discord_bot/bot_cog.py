# Functionality for Discord bot to manage course subscriptions and notifications
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

import discord
from discord.ext import commands, tasks

import redis
import json

class Updates(commands.Cog):
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.conn = redis.Redis(host="localhost", port=6379, db=0)
        self.departments_with_spaces = {"ACENG":"AC ENG", "ARTHIS": "ART HIS", "BIOSCI":"BIO SCI", "COMLIT":"COM LIT",\
                                        "DEVBIO":"DEV BIO", "ECOEVO":"EVO EVO", "EUROST":"EURO ST", "MGMTEP":"MGMT EP",\
                                        "MGMTFE":"MGMT FE", "GLBLME":"GLBL ME", "MGMTHC": "MGMT HC", "I&CSCI":"I&C SCI",\
                                        "INTLST":"INTL ST", "LITJRN":"LIT JRN", "MOLBIO":"MOL BIO", "NETSYS":"NET SYS",\
                                        "NURSCI":"NUR SCI", "PEDGEN":"PED GEN", "PHYSCI":"PHY SCI", "POLSCI":"POL SCI",\
                                        "PUBPOL":"PUB POL", "RELSTD":"REL STD", "SOCSCI":"SOC SCI", "UNIAFF":"UNI AFF",\
                                        "UNISTU":"UNI STU", "VISSTD":"VIS STD"}
        
        self.send_notifications.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to the UCI Course Notification Discord server! \
Please head over to the instructions channel to get started!')
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(str(error))

    @commands.command(help="Subscribes you to recieve notifications for a class.\n\nParameters:\n<department>: \
department of class. Department must not have any spaces. See #instruction for list of all departments.\n<course \
number>: Ex: 32A\n<term>: Fall, Winter, Spring, Summer1, Summer2, or Summer10wk\n<year>: Ex: 2024\n<subscription \
type>: all, num_enrolled, status, or section_added. Deafault is ALL.\n\nExample: !subscribe all compsci 161 fall 2024")
    async def subscribe(self, ctx, department: str, course_num: str, term: str, year: str, sub_type="ALL"):
        sub_type = sub_type.upper()
        department = department.upper()
        term = term.upper()
        course_num = course_num.upper()

        if department in self.departments_with_spaces.keys():
            department = self.departments_with_spaces[department]
        
        # create new subscription and send to new subscription database
        if str(ctx.channel) == "general":
            destination = "general"
        else:
            destination = str(ctx.author)
        new_sub = {"unsubscribe": False, "destination": destination, "subscription":\
                   {"type": sub_type, "author": str(ctx.author), "department": department, \
                    "course_num": course_num, "term": term, "year":year}}
        self.conn.rpush("subscription requests", json.dumps(new_sub))

    @commands.command(help="Removes a subscription that you do not want.\n\nParameters:\n<department>: \
department of class. Department must not have any spaces. See #instruction for list of all departments.\
\n<course number>: Ex: 32A\n<term>: Fall, Winter, Spring, Summer1, Summer2, or Summer10wk\n<year>: Ex: \
2024\n<subscription type>: all, num_enrolled, status, or section_added. Deafault is ALL.\n\nExample: \
!unsubscribe all compsci 161 fall 2024")
    async def unsubscribe(self, ctx, department: str, course_num: str, term: str, year: str, sub_type="ALL"):
        sub_type = sub_type.upper()
        department = department.upper()
        term = term.upper()
        course_num = course_num.upper()

        if department in self.departments_with_spaces.keys():
            department = self.departments_with_spaces[department]

        if str(ctx.channel) == "general":
            destination = "general"
        else:
            destination = str(ctx.author)
        new_sub = {"unsubscribe": True, "destination": destination, \
                   "subscription":{"type": sub_type, "author": str(ctx.author), "department": department, \
                                   "course_num": course_num, "term": term, "year":year}}
        self.conn.rpush("subscription requests", json.dumps(new_sub))

    @commands.command(help="Shows all of your current subscriptions")
    async def see_subscriptions(self, ctx):
        all_subscriptions = [json.loads(x) for x in self.conn.smembers("subscriptions")]
        this_subscriptions = []
        for sub in all_subscriptions:
            if sub["author"] == str(ctx.author):
                this_subscriptions.append(f'Subscription Type: {sub["type"]} Course: {sub["department"]} \
                                          {sub["course_num"]} {sub["term"]} {sub["year"]}')
        if this_subscriptions:
            await ctx.send(f"{ctx.author}, you are subscribed to:\n-" + "\n-".join(this_subscriptions))
        else:
            await ctx.send(f"{ctx.author}, you are not subscribed to any courses.")

    @tasks.loop(seconds=1)
    async def send_notifications(self):
        while notification := self.conn.lpop("notifications"):
            notification = json.loads(notification)
            print(f'Notification:\n -Destination: {notification["destination"]}\n -Text: {notification["text"]}')

            if notification["destination"] == "general":
                channel = None
                for c in self.guild.channels:
                    if c.name == "general" and isinstance(c, discord.TextChannel):
                        channel = c
                if channel:
                    await channel.send(notification["text"])
                else:
                    print("Could not find General Channel")
            else:
                # notification["destination"] is the name of the member to dm
                member = None
                for m in self.guild.members:
                    if m.name == notification["destination"]:
                        member = m
                if member:
                    await member.create_dm()
                    await member.dm_channel.send(notification["text"])
                else:
                    print(f"Could not find member: {notification['destination']} Channel")
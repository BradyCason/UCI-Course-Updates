# UCI Course Updates
A collection of scripts and servers that work together to allow UCI students to subscribe to certain events pertaining to UCI course registration, such as number of enrolled members, courses switching from OPEN to WAITLISTING, sections being added, and more!

# Using the Service
- Join the UCI Course Notifications Discord Server: https://discord.gg/UCr7dCyT26
- Head over to the #instructions channel to see how to use it.
- Interact with the Course Updates Bot by typing one of the following commands:
  - !help
  - !subscribe  [department] [course number] [term] [year]  [subscription type]
  - !unsubscribe [department] [course number] [term] [year]  [subscription type]
  - !see_subscriptions
- See the discord server for more

# Running on your own computer
- Create a new Discord Server and create a bot for it on the [Discord Developer Platform](https://discord.com/developers/docs/intro)
- Create a file named ".env" in the "discord_bot" folder. In the file write:
`DISCORD_TOKEN=<Discord bot token>
DISCORD_GUILD=<Discord seerver name>`
- Then just run run_uci_course_notifications.py


# How it Works
- run_uci_course_notifications.py is a script to run the whole application at once. It creates a local [redis](https://redis.io/docs/latest/develop/connect/clients/python/) (Remote Dictionary Server) server and manages and runs three threads: discord_bot, subscription_request_manager, and course_watcher
- discord_bot is a bot that interacts with the discord server using [Discord API](https://discordpy.readthedocs.io/en/stable/). It sends new course subscriptions to redis, and it recieves notifications from redis.
- subscription_request_manager is a script that manages incoming subscription requests from the redis server.
- course_watcher is a script that watches for course changes for all subscriptions and pushes notifications to redis

# Disclaimer
The bot will only work if the script is running on my computer. If the Course Updates Bot appears offline, then the script is not running, and you will not receive any notifications or be able to submit any subscriptions. If the bot is offline, and you would like to use the service, please message me in the #⁠general channel and ask me to run the bot. I will do my best to run it whenever you guys need it.
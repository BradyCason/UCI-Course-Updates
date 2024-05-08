# discord_bot
The discord_bot is the user's interface to interact with the service. Users send the bot commands to subscribe and unsubscribe from courses, and the bot DM's them notifications.

# bot_initializer.py
This script initializes a discord bot and connects it the the UCI Course Updates Discord server. It notifies users that it is online. It uses the Discord API.

# bot_cog.py
This script defines the functionality of the bot. It defines the Discord commands and sends the user notifications that appear in the queue on the redis server.
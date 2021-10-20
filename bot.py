"""
This is a tutorial from 
https://vcokltfre.dev/tutorial/
"""

import os
from dotenv import load_dotenv
import discord 
from discord.ext import commands 


# load token and guild information 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# enable bot to track presence of members 
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", guild_subscriptions=True, intents=intents) 

# load commands and run bot 
bot.load_extension("cog_commands") #no need for .py extension 
bot.run(TOKEN)
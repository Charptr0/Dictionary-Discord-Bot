import discord
from discord.ext import commands
import dictionary

token = ""

bot = commands.Bot(command_prefix= "!db")
bot.remove_command("help")


@bot.event
async def on_ready():
    print("The bot is ready")

@bot.command("define")
async def define(ctx):
    pass


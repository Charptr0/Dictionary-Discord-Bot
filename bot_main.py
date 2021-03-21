import discord
from discord import embeds
from discord.ext import commands
import dictionary

token = ""

bot = commands.Bot(command_prefix= "db!")
bot.remove_command("help")

@bot.event
async def on_ready():
    print("The bot is ready")

@bot.command("define")
async def define(ctx, unknownWord):
    word = dictionary.getHTML(unknownWord)
    if word == "404" or word.definitions() == "No definitions found":
        await ctx.send("error")

    else: await ctx.send(str(word.definitions()))


bot.run(token)

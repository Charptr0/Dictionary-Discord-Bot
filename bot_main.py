import discord
from discord import embeds
from discord.ext import commands
import dictionary

token = ""

bot = commands.Bot(command_prefix= "db!")
bot.remove_command("help")


def createWordEmbed(word): #If the word exists, create an embed message that contains the name, pos, definition, synonyms and antonyms of the word
    embed_message = discord.Embed(title="Dictionary Bot", description="Here is what I found:", colour=discord.Colour.blue())
    embed_message.add_field(name="Word", value=word.name(), inline=False)
    embed_message.add_field(name="Part of Speech", value=word.partOfSpeech(), inline=False)
    embed_message.add_field(name="Definitions", value=word.definitions(), inline=False)
    embed_message.add_field(name="Synonyms", value=word.synonyms(), inline=False)

    if word.antonyms() != None:
        embed_message.add_field(name="Antonyms", value=word.antonyms(), inline=False)

    return embed_message

def createWordErrorEmbed(error_message): #If an error occurs, create an embed message to inform the user
    embed_message = discord.Embed(title="Dictionary Bot", description="Something went wrong and I cannot find what you are looking for", colour=discord.Colour.orange())
    embed_message.add_field(name="Error Message:", value=error_message, inline=False)

    if "404" in error_message:
        embed_message.add_field(name="Possible Soultion:", value='''Please check your spelling of the word or phrase and try again.''', inline=False)

    embed_message.set_footer(text="Please contact the server mods if you are having trouble")

    return embed_message

@bot.event
async def on_ready():
    print("The bot is ready")

@bot.command("define")
async def define(ctx, unknownWord):
    word = dictionary.getDictionaryWordHTML(unknownWord)
    if word == "404 Webpage cannot be found" or word.definitions() == "No definitions found":
        await ctx.send(embed=createWordErrorEmbed(word))

    else: await ctx.send(embed=createWordEmbed(word))

@bot.command("udefine")
async def udefine(ctx, *unknownPhrase):
    urban_phrase = dictionary.getUrbanHTML(unknownPhrase)

    if urban_phrase == "404 Webpage cannot be found":
        await ctx.send(embed=createWordErrorEmbed(urban_phrase))
    
    else: await ctx.send("connected")


bot.run(token)



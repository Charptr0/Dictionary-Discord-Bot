import discord
from discord import embeds
from discord.ext import commands
import dictionary

token = "" #put your token here

#boiler code
bot = commands.Bot(command_prefix= "db!")
bot.remove_command("help")
#

def createWordEmbed(word : dictionary.Word): #If the word exists, create an embed message that contains the name, pos, definition, synonyms and antonyms of the word
    embed_word_message = discord.Embed(title="Dictionary Bot", description="Here is what I found:", colour=discord.Colour.blue())
    embed_word_message.add_field(name="Word", value=word.name(), inline=False)
    embed_word_message.add_field(name="Part of Speech", value=word.partOfSpeech(), inline=False)
    embed_word_message.add_field(name="Definitions", value=word.definitions(), inline=False)
    embed_word_message.add_field(name="Synonyms", value=word.synonyms(), inline=False)

    if word.antonyms() != None:
        embed_word_message.add_field(name="Antonyms", value=word.antonyms(), inline=False)

    return embed_word_message

def createWordErrorEmbed(error_message): #If an error occurs, create an embed message to inform the user
    embed_error_message = discord.Embed(title="Dictionary Bot", description="Something went wrong and I cannot find what you are looking for", colour=discord.Colour.orange())
    embed_error_message.add_field(name="Error Message:", value=error_message, inline=False)

    if "404" in error_message:
        embed_error_message.add_field(name="Possible Soultion:", value='''Please check your spelling of the word or phrase and try again.''', inline=False)

    embed_error_message.set_footer(text="Please contact the server mods if you are having trouble")

    return embed_error_message

def createUrbanPhraseEmbed(urban_phrase : dictionary.UrbanWord): #same deal with the word embed, but with urban phrases instead
    embed_urban_message = discord.Embed(title="Dictionary Bot", description="Here is what I found:", colour=discord.Colour.blue())
    embed_urban_message.add_field(name="Word/Phrase", value=urban_phrase.phrase(), inline=False)
    embed_urban_message.add_field(name="Top Definition", value=urban_phrase.definition(), inline=False)
    embed_urban_message.add_field(name="Contributor", value=urban_phrase.author(), inline=False)

    return embed_urban_message


@bot.event
async def on_ready():
    print("The bot is ready") 

'''
help()
    - create a help menu to list all the commands
'''
@bot.command("help")
async def help(ctx):
    embedded_help_message = discord.Embed(title="Dictionary Bot", description="Commands:", colour=discord.Colour.blue())
    embedded_help_message.add_field(name="db!define", value="Define a word that is supported by the english dictionary", inline=False)
    embedded_help_message.add_field(name="db!udefine", value="Define a word or a phrase that is supported by urban dictionary", inline=False)

    await ctx.send(embed=embedded_help_message)

'''
define()
    - gets the information from dictionary.com
    - create an instance of the Word 
    - grab the info from the Word class
    - if the message is 404, print send a error message
    - else send the message along with the name, definition, part of speech, synonyms, and antonyms
    - delete the instance of the class 
'''
@bot.command("define")
async def define(ctx, unknownWord):
    word = dictionary.getDictionaryWordHTML(unknownWord) #create a instance of the Word
    if word == "404 Webpage cannot be found" or word.definitions() == "No definitions found": #if the website 404
        await ctx.send(embed=createWordErrorEmbed(word)) #send the error message

    else: await ctx.send(embed=createWordEmbed(word)) #if everything is ok, send the embedded message

    word.delete() #delete the instance

'''
udefine()
    - gets the information from urbandictionary.com
    - create an instance of the UrbanWord 
    - grab the info from the UrbanWord class
    - if the message is 404, send a error message
    - else send the message along with the name, definition, contributor and the date
    - delete the instance of the class 
'''
@bot.command("udefine")
async def udefine(ctx, *unknownPhrase):
    urban_phrase = dictionary.getUrbanHTML(unknownPhrase) #create a instance of the UrbanWord

    if urban_phrase == "404 Webpage cannot be found": #if the website 404
        await ctx.send(embed=createWordErrorEmbed(urban_phrase)) #send the error message
    
    else: await ctx.send(embed=createUrbanPhraseEmbed(urban_phrase)) #if everything is ok, send the embedded message

    urban_phrase.delete() #delete

bot.run(token) #Start the bot
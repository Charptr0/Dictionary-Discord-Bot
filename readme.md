# Dictionary Discord Bot <img src="https://i.imgur.com/NBbOMgg.png" width="150px" align="right"></img>

Finding the meaning behind words and phrases directly through Discord.

## Features
**For official English words**: <img src="https://i.imgur.com/1bD29dw.png" width="250px" align="right"></img>

- If the connection is successful, the bot will display:
  - The Name of the Word
  - Top Three Definitions
  - Part of Speech
  - Up to three Synonyms and Antonyms* (*if the word has antonyms)
- All information will be grabbed from https://dictionary.com

<hr>

**For phrases and modern slang**: <img src="https://i.imgur.com/nrwLGD9.png" width="250px" align="right"></img>
- If the connection is successful, the bot will display:
  - The Top Definition
  - The Contributor
  - The Contribution Date
- All information will be grabbed from https://urbandictionary.com

<hr>

**If the bot cannot get a connection to dictionary or urbandictionary**:<img src="https://i.imgur.com/zfFBT5i.png" width="450px" align="right"></img>
- The bot will display an error message:
  - Notifying the user that there is an connection issue
  - Printing out the error message
  - Listing some possible solutions

- Most of the errors are caused by the user searching up a word or a phrase that does not exist

## Commands
<code>db!define [word]</code>

Look up a word from dictionary.com

<code>db!udefine [word/phrase]</code>

Look up a word or a phrase from urbandictionary.com

## Installation
<div><strong>The Basics</strong>
<ol>
  <li>Create a <a href="https://discord.com/">discord account</a></li>
  <li>Create an empty bot from the <a href="https://discord.com/developers/applications">Discord Developer Portal</a></li>
  <li>Invite the empty bot to your server</li>
</ol>
</div>

<div><strong>Starting the bot from scratch</strong>
<ol>
  <li>Clone this repository</li>
  <li>Install all the dependencies</li>
  <li>Copy your bot token and paste it into the token variable (The token has to be a string)</li>
  <li>Start the bot</li>
</ol>
</div>

**Starting the bot using Docker**
1. Clone this repository
2. Copy your bot token and paste it into the token variable (The token has to be a string)
3. Run the Dockerfile

## Modules/Dependencies
- Discord API
- BeautifulSoup
- Urllib.request

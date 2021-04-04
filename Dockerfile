FROM python:3.8

WORKDIR /bot

#Install the dependencies
RUN pip install discord
RUN pip install bs4

#Copy all files to /bot 
COPY . .

#Start the bot
ENTRYPOINT [ "python", "bot_main.py" ]
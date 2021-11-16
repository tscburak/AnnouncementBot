# This Python file uses the following encoding: utf-8

import os
import discord
import urllib3
import keep_alive
from replit import db
from messageSender import notifications
from messageSender import commandResponse
import check_all_time

# replit database
if "channels" in db.keys():
  allChannels = db["channels"]
else:
  db["channels"] = []

# ignore the warnings
urllib3.disable_warnings()

# import discord client to manage bot
client = discord.Client()


# displays when the bot connect the server
@client.event
async def on_ready():
    print(f'{client.user} is now online!')




# responses the commands
@client.event
async def on_message(message):

    # make sure bot doesn't respond to it's own messages to avoid infinite loop
    
    if message.author == client.user:
        return

    # shares the help text
    if message.content.startswith(f'a$help'):
      await commandResponse.helpCommand(message)

    # register the channel id to database to start sharing the announce
    if message.content.startswith(f'a$start'):

      channelid = message.channel.id
      if channelid in db["channels"]:
        await notifications.startAgainNotification(message)
      else:
        await notifications.startNotification(message)
        allChannels.append(channelid)
        db["channels"] = allChannels

    # remove the channel id from database to stop sharing announce
    if message.content.startswith(f'a$stop'):
      
      channelid = message.channel.id
      if channelid in db["channels"]:
        await notifications.stopNotification(message)
        allChannels.remove(channelid)
        db["channels"] = allChannels
      else:
        await notifications.stopAgainNotification(message)
  


keep_alive.keep_alive()

# bot token
my_secret = os.environ['token']

# start the loop CheckAllTime
check_all_time.checkAllTime.start(client)
client.run(my_secret)
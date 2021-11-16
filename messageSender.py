import discord


# This class for sending message in embed style

class notifications:
  async def startNotification(message):
    embed = discord.Embed(title="The service has been started in this channel!", description="I will share the announcement as soon as the new one comes.\nPlease use `a$help` command when you need help.", color = 0x0ab4b1)
    await message.channel.send(embed=embed)

  async def startAgainNotification(message):
    embed = discord.Embed(title="The service has been started already!",description="You can stop the service `a$stop` command.",color = 0x808080)
    await message.channel.send(embed=embed)

  async def stopNotification(message):
    embed = discord.Embed(title="The service has been stopped.", description="I will not share the announcement anymore. You can start the service `a$start` command later.", color = 0xFF0000)
    await message.channel.send(embed=embed)

  async def stopAgainNotification(message):
    embed = discord.Embed(title="The service has been stopped already or never started.",description="You can start the service `a$start` command.", color = 0x808080)
    await message.channel.send(embed=embed)



class commandResponse:
  async def helpCommand(message):
    embed = discord.Embed(title="Help",color=0x0ab4b1)
    embed.add_field(name="About Bot",value="The bot is checking 3 different website *(SKS Website, Main Website, Faculty Website)* to get the announcements. Please contact us if you need any help or want to share your experiments/suggestions.\n\n", inline=False)
    embed.add_field(name="a$start",value="starts to sharing announcement in current channel\n\n", inline=True)
    embed.add_field(name="a$stop",value="stops to sharing the announcement in current channel\n\n", inline=True)
    embed.add_field(name="Contact",value="buraktasci2001@gmail.com", inline=False)
    await message.channel.send(embed=embed)


class announcements:
  # share the announcement on the channel which have in the parameter
  async def sharing(channel,titleOfAnnounce,descriptionOfAnnounce,linkOfAnnounce, imgOfAnnounce,thumbimg):
    for i in range (0, len(titleOfAnnounce)):
    
      embed = discord.Embed(title=titleOfAnnounce[i], url=linkOfAnnounce[i], description='%.300s' % descriptionOfAnnounce[i], color = 0x0ab4b1)
      embed.set_image(url=imgOfAnnounce[i])
      embed.set_thumbnail(url=thumbimg)
      await channel.send(embed=embed)
    
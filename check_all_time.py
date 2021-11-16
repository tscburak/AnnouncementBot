from discord.ext import tasks
import asyncio
import search_uu
from messageSender import announcements
from replit import db
import discord

if "channels" in db.keys():
  allChannels = db["channels"]
else:
  db["channels"] = []

sharing = announcements.sharing
client = discord.Client()

# checks the websites each 5 minutes and share if there is new one 
@tasks.loop(seconds = 360)
async def checkAllTime(client):

  await asyncio.sleep(10)
  allChannels = db["channels"]

  # define the scrape class 
  scrape = search_uu.scrape()

  # searchs faculty website TR
  titleOfAnnounce_mdbfTR,descriptionOfAnnounce_mdbfTR,linkOfAnnounce_mdbfTR, imgOfAnnounce_mdbfTR = scrape.search_uu_mdbf(url="https://uskudar.edu.tr/mdbf/tr/announcements")

  # searchs faculty website EN
  titleOfAnnounce_mdbfEN,descriptionOfAnnounce_mdbfEN,linkOfAnnounce_mdbfEN, imgOfAnnounce_mdbfEN = scrape.search_uu_mdbf(url="https://uskudar.edu.tr/mdbf/en/announcements")

  # searchs main website EN
  titleOfAnnounce_mainEN,descriptionOfAnnounce_mainEN,linkOfAnnounce_mainEN, imgOfAnnounce_mainEN = scrape.search_uu_main(url="https://uskudar.edu.tr/en/icerikler/duyurular/")

  # searchs main website TR
  titleOfAnnounce_mainTR,descriptionOfAnnounce_mainTR,linkOfAnnounce_mainTR, imgOfAnnounce_mainTR = scrape.search_uu_main(url="https://uskudar.edu.tr/tr/icerikler/duyurular/")

  # searchs SKS website
  titleOfAnnounce_sks,descriptionOfAnnounce_sks,linkOfAnnounce_sks, imgOfAnnounce_sks = scrape.search_uu_sks(url="https://sks.uskudar.edu.tr/duyurular?page=1")

  # here is the sharing section
  for channelid in allChannels:
    # tries to get channel id, if a channel deleted from the server it throw AttributeError and delete the channel from database
    try:
      channel = client.get_channel(channelid)
      id = channel.id
    except AttributeError:
      print("Silinen kanal mevcut")
      allChannels.remove(channelid)
      continue

    # shares the announcement according to parameters (channel, title, description, link, img, icon)

    await sharing(channel,titleOfAnnounce_mdbfTR,descriptionOfAnnounce_mdbfTR,linkOfAnnounce_mdbfTR, imgOfAnnounce_mdbfTR,"http://www.globalacademia.com/wp-content/uploads/%C3%9Csk%C3%BCdar-%C3%9Cniversitesi-Global-Academia.png")
    await sharing(channel,titleOfAnnounce_mdbfEN,descriptionOfAnnounce_mdbfEN,linkOfAnnounce_mdbfEN, imgOfAnnounce_mdbfEN,"http://www.globalacademia.com/wp-content/uploads/%C3%9Csk%C3%BCdar-%C3%9Cniversitesi-Global-Academia.png")
    await sharing(channel,titleOfAnnounce_mainEN,descriptionOfAnnounce_mainEN,linkOfAnnounce_mainEN, imgOfAnnounce_mainEN,"http://www.globalacademia.com/wp-content/uploads/%C3%9Csk%C3%BCdar-%C3%9Cniversitesi-Global-Academia.png")
    await sharing(channel,titleOfAnnounce_mainTR,descriptionOfAnnounce_mainTR,linkOfAnnounce_mainTR, imgOfAnnounce_mainTR,"http://www.globalacademia.com/wp-content/uploads/%C3%9Csk%C3%BCdar-%C3%9Cniversitesi-Global-Academia.png")
    await sharing(channel,titleOfAnnounce_sks,descriptionOfAnnounce_sks,linkOfAnnounce_sks, imgOfAnnounce_sks,"https://i.hizliresim.com/5ljw48x.png")
    
    print(str(channel)+": "+str(id))


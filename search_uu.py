# This Python file uses the following encoding: utf-8

from bs4 import BeautifulSoup
from replit import db
import ssl
import requests
from datetime import datetime
import pytz

class scrape():

  

  # sets the link database and current date 
  def __init__(self):
    tz_TR = pytz.timezone('Europe/Istanbul') 
    datetime_TR,_ = str(datetime.now(tz_TR)).split()
    y,m,d=datetime_TR.split("-")
    self.datetime_TR = d+"."+m+"."+y

    if "links" in db.keys():
      courses = db["links"]
    else:
        db["links"] = {}
      
    self.courses = db["links"]


  # return the website html codes
  def request_url(self,url):
    
    ssl._create_default_https_context = ssl._create_unverified_context    
    r = requests.get(url, verify=False)
    html_soup = BeautifulSoup(r.text,'html.parser')

    return html_soup


  # searchs the uu main website, URL decides which website searching, EN or TR 
  def search_uu_main(self,url):

    ssl._create_default_https_context = ssl._create_unverified_context    

    html_soup = scrape().request_url(url)

    # select the all announce division
    announcements = html_soup.find_all('div', class_="card",limit=5)

    AnLink = []
    AnDescription = []
    AnTitle = []
    AnImg = []
    AnDate = []


    for announce in announcements:
      head = announce.find('div', class_="card-body")
      text = head.find('a')
      description = head.find('p', class_="card-text")
      img = announce.find('img')


      titleOfAnnounce = text.text
      linkOfAnnounce = text.get("href")

      soup_date = scrape().request_url(linkOfAnnounce)
      time = soup_date.find("div",class_="date-added").text

      # fixes the date format because in this website date format like: 16.11.2021 - 09:18
      dateOfAnnounce,_ = time.split("-")
      dateOfAnnounce = dateOfAnnounce[1:]
      # adds the date on the description
      descriptionOfAnnounce = "**{}**\n\n".format(dateOfAnnounce)+str(description.text)[1:]
      

      # if the img url has 'assets' it's not displaying on the discord, so I used imageholder for that
      if (img.get("data-src").__contains__("assets")):
        photoOfAnnounce = "https://i.hizliresim.com/e89qzvg.jpg"
      else:
        photoOfAnnounce = img.get("data-src")

      
      # if the link of announce is not in the database it will be shared
      # if the link is in database there is one more condition to decide, if today date match announce date it will be passed and won't be shared. However link has a different date before but now its date is today that means this is new. I know that is complicated a bit but let me explain this way:
      # When some announce update after days the program doesn't recognize that is new because links are same. So I have to decide to define a new algorithm. I hope I was able to explain.  
      if linkOfAnnounce in db["links"]:
        if db["links"][linkOfAnnounce].startswith(self.datetime_TR):
          pass
        elif dateOfAnnounce.startswith(self.datetime_TR):
            AnTitle.append(titleOfAnnounce)
            AnDescription.append(descriptionOfAnnounce)
            AnLink.append(linkOfAnnounce)
            AnImg.append(photoOfAnnounce)
            AnDate.append(dateOfAnnounce[1:])
            db["links"][linkOfAnnounce] = dateOfAnnounce
            self.courses = db["links"]
         

      elif dateOfAnnounce.startswith(self.datetime_TR):
          AnTitle.append(titleOfAnnounce)
          AnDescription.append(descriptionOfAnnounce)
          AnLink.append(linkOfAnnounce)
          AnImg.append(photoOfAnnounce)
          AnDate.append(dateOfAnnounce[1:])

          db["links"][linkOfAnnounce] = dateOfAnnounce
          self.courses = db["links"]

    
    # Display the all variable that we need and return them
    print(AnTitle, AnDescription, AnLink, AnImg, AnDate)
    return (AnTitle, AnDescription, AnLink, AnImg)  


  def search_uu_mdbf(self,url):
    
    # I had to define a dictionary to decide the dates. Because in the website they defined the months with shortcuts.
    months = {"OCA":"1","ŞUB":"2","MAR":"3","NİS":"4","MAY":"5","HAZ":"6","TEM":"7",
    "AĞU":"8","EYL":"9","EKI":"10","KAS":"11","ARA":"12","JAN":"1","FEB":"2","MAR":"3","APR":"4","MAY":"5","JUNE":"6","JULY":"7",
    "AUG":"8","SEPT":"9","OCT":"10","NOV":"11","DEC":"12"}

    urlMainMenu = "https://uskudar.edu.tr"

    html_soup = scrape().request_url(url)

    announcements = html_soup.find_all('div', class_="notification-item",limit=5)

    AnLink = []
    AnDescription = []
    AnTitle = []
    AnImg = []
    AnDate = []

    for announce in announcements:
      
      head = announce.find('h3')
      text = announce.find('a')
      description = announce.find('p')
      time = announce.find('div',class_ = "date").text
      linkOfAnnounce = urlMainMenu + text.get("href")

      # fixes the date format
      d,m,y = time.split()
      dateOfAnnounce = d+"."+months[m.upper()]+"."+y

      titleOfAnnounce = head.text

      # the program takes all the text from the announcement in the only faculty website. So sometimes it can be too long and discord doesn't allow to share too long message. That's why I tried to put limit for that. Also adds the date on the description
      if (len(description.text) >= 300):
        descriptionOfAnnounce = "**{}**\n\n".format(dateOfAnnounce) +'%.270s' % description.text + "..."
      else:
        descriptionOfAnnounce = "**{}**\n\n".format(dateOfAnnounce)+ description.text


      # Decides if announce is new
      if linkOfAnnounce in db["links"]:
        if db["links"][linkOfAnnounce].startswith(self.datetime_TR):
          pass

        elif dateOfAnnounce.startswith(self.datetime_TR):
            AnTitle.append(titleOfAnnounce)
            AnDescription.append(descriptionOfAnnounce)
            AnLink.append(linkOfAnnounce)
            AnImg.append("https://i.hizliresim.com/lvlhdr0.jpg")
            AnDate.append(dateOfAnnounce)

            db["links"][linkOfAnnounce] = dateOfAnnounce
            self.courses = db["links"]


      elif dateOfAnnounce.startswith(self.datetime_TR):
          AnTitle.append(titleOfAnnounce)
          AnDescription.append(descriptionOfAnnounce)
          AnLink.append(linkOfAnnounce)
          AnImg.append("https://i.hizliresim.com/lvlhdr0.jpg")
          AnDate.append(dateOfAnnounce)

          db["links"][linkOfAnnounce] = dateOfAnnounce
          self.courses = db["links"]

    # Display the all variable that we need and return them
    print(AnTitle, AnDescription, AnLink, AnImg, AnDate)
    return (AnTitle, AnDescription, AnLink, AnImg)


  def search_uu_sks(self,url):
    

    ssl._create_default_https_context = ssl._create_unverified_context

    html_soup = scrape().request_url(url)

    announcements = html_soup.find_all('div', class_="blog-list-post clearfix",limit=5)

    AnLink = []
    AnDescription = []
    AnTitle = []
    AnImg = []
    AnDate = []

    for announce in announcements:
      head = announce.find('h5', class_="blog-list-title")
      text = head.find('a')
      description = announce.find('p', class_="blog-list-meta small-text")
      time = announce.find('time')
      dateOfAnnounce,_ = time.get("datetime").split()
      titleOfAnnounce = text.text
      
      linkOfAnnounce = text.get("href")

      # fixes the date format
      y,m,d = dateOfAnnounce.split("-")
      dateOfAnnounce = d+"."+m+"."+y

      # adds the date on the description
      descriptionOfAnnounce = "**{}**\n\n".format(dateOfAnnounce) + description.text
      
      # Decides if announce is new
      if linkOfAnnounce in db["links"]:
        if db["links"][linkOfAnnounce].startswith(self.datetime_TR):
          pass
        elif dateOfAnnounce.startswith(self.datetime_TR):
            AnTitle.append(titleOfAnnounce)
            AnDescription.append(descriptionOfAnnounce)
            AnLink.append(linkOfAnnounce)
            AnImg.append("https://i.hizliresim.com/ajceetm.jpg")
            AnDate.append(dateOfAnnounce)

            db["links"][linkOfAnnounce] = dateOfAnnounce
            self.courses = db["links"]


      elif dateOfAnnounce.startswith(self.datetime_TR):
        AnTitle.append(titleOfAnnounce)
        AnDescription.append(descriptionOfAnnounce)
        AnLink.append(linkOfAnnounce)
        AnImg.append("https://i.hizliresim.com/ajceetm.jpg")
        AnDate.append(dateOfAnnounce)
        
        db["links"][linkOfAnnounce] = dateOfAnnounce
        self.courses = db["links"]

    # Display the all variable that we need and return them
    print(AnTitle, AnDescription, AnLink, AnImg, AnDate)
    return (AnTitle, AnDescription, AnLink, AnImg)

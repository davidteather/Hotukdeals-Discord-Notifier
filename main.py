import discord
import asyncio
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


with open('settings.json') as data:
    settings = json.load(data)

    min_upvotes = int(settings["min_upvotes"])
    max_upvotes = int(settings["max_upvotes"])

    base_url = settings["base_url"]
    pages_to_index = int(settings["pages_to_index"])
    discord_api_key = settings["discord_api_token"]

    min_price = float(settings["min_price"])
    max_price = float(settings["max_price"])

    channel_id = int(settings["discord_channel_id"])

    time_interval_seconds = int(settings["time_interval_seconds"])


class MyClient(discord.Client):
    def __init__(self, channel, *args, **kwargs):
        self.outOfStock = []
        self.checkUrls = []
        self.channelID = channel
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    # Check deals

    def checkDealsBeautifulSoup(self, url):
        # Imports
        import requests
        from bs4 import BeautifulSoup
        import json
        from requests.adapters import HTTPAdapter
        import random

        # Loads JSON and vars
        with open('settings.json') as data:
            settings = json.load(data)

            min_upvotes = int(settings["min_upvotes"])
            max_upvotes = int(settings["max_upvotes"])

            min_price = float(settings["min_price"])
            max_price = float(settings["max_price"])

            proxyvar = settings['proxy']

        # Loads proxies
        with open('proxies.txt', 'r') as proxiesf:
            proxies = proxiesf.readlines()

        with open('httpsProxy.txt', 'r') as proxieshttps:
            httpsProxies = proxieshttps.readlines()

        # Picks random proxy
        proxy1 = random.choice(proxies)
        httpsProxy = random.choice(httpsProxies)


        returnMsgs = []
        newArray = []

        # Reads already used things
        with open('data/usedLinks.txt', 'r') as data:
            usedArray = data.readlines()

        # Sets up proxy
        #session = requests.session()

        if proxyvar == "True" or proxyvar == True:
            proxy = {"http": "http://" + proxy1,
                    "https": "https://" + httpsProxy}

            page = requests.get(url, proxies=proxy)
        else:
            page = requests.get(url)


        soup = BeautifulSoup(page.text, 'html.parser')
        # Tries to get things
        listings = soup.find_all(
            'article', attrs={'data-handler': 'history'})
        upvotes = soup.find_all('span', attrs={'class': 'cept-vote-temp'})
        pricing = soup.find_all('span', attrs={'class': 'thread-price'})
        urls = soup.find_all(
            'a', attrs={'class': 'cept-thread-image-link'})
        var = True

        if var == True:
            upvotesIndex = 0
            index = 0
            for x in range(0, len(listings)):
                try:
                    upvote = upvotes[upvotesIndex].text.strip().replace(
                        " ", "").replace("°", "").replace("\n", "")
                    if "Deal" in upvote or "alerts" in upvote:
                        upvotesIndex += 1
                        upvote = upvotes[upvotesIndex].text.strip().replace(
                            " ", "").replace("°", "").replace("\n", "")

                except:
                    upvote = 0


                try:
                    price = pricing[index].text.strip().replace("£", "")
                except:
                    price = 0
                try:
                    url = urls[index].get('href')
                except:
                    url = None
                if price != "FREE":
                    try:
                        price = float(price.replace(",", ""))
                    except:
                        price = 0
                else:
                    price = 0

                if min_price <= price <= max_price:
                    if min_upvotes <= int(upvote) <= max_upvotes:
                        if url != None:
                            if url + "\n" not in usedArray and "/deals/" in url:
                                # Return Message
                                message = url + " Satisfies your deal criteria. It is at " + \
                                    str(upvote) + \
                                    " degrees and costs £" + str(price)

                                # "Apple iPad Air 3 10.5 2019 model, 64 GB 256 GB"
                                # "https://www.hotukdeals.com/deals/ipad-air-2019-3293151"
                                # "\n**Price**: $price \n**Temperature**: $upvote"
                                r = requests.get(url, proxies=proxy) 
                                soup2 = BeautifulSoup(r.text, 'html.parser')
                                
                                image = soup2.find('img', attrs={'class': 'thread-image'})
                                try:
                                    thumbnail = image2.get('src')
                                except:
                                    thumbnail = "https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fsitechecker.pro%2Fwp-content%2Fuploads%2F2017%2F12%2F404.png&f=1&nofb=1"
                                
                                
                                try:
                                    title = image.get('alt')
                                except:
                                    title = "Error"
                                
                                if title != None and thumbnail != None:
                                    json = {
                                        "title": title,
                                        "url": url,
                                        "temp": int(upvote),
                                        "price": float(price),
                                        "thumbnail": thumbnail
                                    }
                                elif title == None and thumbnail != None:
                                    json = {
                                        "title": "Error",
                                        "url": url,
                                        "temp": int(upvote),
                                        "price": float(price),
                                        "thumbnail": thumbnail
                                    }

                                elif title != None and thumbnail == None:
                                    json = {
                                        "title": title,
                                        "url": url,
                                        "temp": int(upvote),
                                        "price": float(price),
                                        "thumbnail": "https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fegyptianstreets.com%2Fwp-content%2Fuploads%2F2017%2F07%2F404.jpg&f=1&nofb=1"
                                    }

                                elif title == None and thumbnail == None:
                                    json = {
                                        "title": "Error",
                                        "url": url,
                                        "temp": int(upvote),
                                        "price": float(price),
                                        "thumbnail": "https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fegyptianstreets.com%2Fwp-content%2Fuploads%2F2017%2F07%2F404.jpg&f=1&nofb=1"
                                    }

                                returnMsgs.append(json)
                                usedArray.append(url)
                                newArray.append(url)
                upvotesIndex += 1
                index += 1

        # Saves new logged files
        with open('data/usedLinks.txt', 'a') as fileObj:
            for line in newArray:
                fileObj.write(line + "\n")

        # Returns stuff
        return returnMsgs

    # On start

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    # On message

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

    # Background manager

    async def my_background_task(self):
        from discord import Embed
        import discord
        await self.wait_until_ready()
        channel = self.get_channel(int(channel_id))
        while not self.is_closed():
            for page in range(0, int(pages_to_index)):
                print('checking page ' + str(page))
                try:
                    res = self.checkDealsBeautifulSoup(
                        base_url + "?page=" + str(page))
                except:
                    res = []
                if res != []:
                    for msg in res:
                        try:
                            embed = discord.Embed(
                                title=msg['title'], url=msg['url'])
                            embed.set_thumbnail(url=msg['thumbnail'])
                            embed.add_field(
                                name="Price", value=msg['price'], inline=True)
                            embed.add_field(name="Temperature",
                                            value=msg['temp'], inline=True)
                            # await self.bot.say(embed=embed)

                            # await self.bot.say(embed=embed)
                            await channel.send(embed=embed)
                        except:
                            print('Failed on')
                            print(msg)
            await asyncio.sleep(int(time_interval_seconds))


# Main
client = MyClient(channel_id)
client.run(discord_api_key)

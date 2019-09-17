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
        import random

        # Loads JSON and vars
        with open('settings.json') as data:
            settings = json.load(data)

            min_upvotes = int(settings["min_upvotes"])
            max_upvotes = int(settings["max_upvotes"])

            min_price = float(settings["min_price"])
            max_price = float(settings["max_price"])

        # Loads proxies
        with open('proxies.txt', 'r') as proxies:
            proxies = proxies.readlines()

        # Picks random proxy
        proxy = random.choice(proxies)

        returnMsgs = []
        newArray = []

        # Reads already used things
        with open('data/usedLinks.txt', 'r') as data:
            usedArray = data.readlines()

        # Sets up proxy
        proxies = {
            "http": "http://" + proxy,
            "https": "https://" + proxy,
        }

        page = requests.get(url, proxies=proxy)
        soup = BeautifulSoup(page.text, 'html.parser')
        var = False

        # Tries to get things
        try:
            listings = soup.find_all(
                'article', attrs={'data-handler': 'history'})
            upvotes = soup.find_all('span', attrs={'class': 'cept-vote-temp'})
            pricing = soup.find_all('span', attrs={'class': 'thread-price'})
            urls = soup.find_all(
                'a', attrs={'class': 'cept-thread-image-link'})
            var = True
        except:
            var = False

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
                            if url + "\n" not in usedArray:
                                # Return Message
                                message = url + " Satisfies your deal criteria. It is at " + \
                                    str(upvote) + \
                                    " degrees and costs £" + str(price)
                                returnMsgs.append(message)
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
        await self.wait_until_ready()
        channel = self.get_channel(int(channel_id))
        while not self.is_closed():
            for page in range(0, int(pages_to_index)):
                print('checking page ' + str(page))
                res = self.checkDealsBeautifulSoup(
                    base_url + "?page=" + str(page))
                if res != []:
                    for msg in res:
                        await channel.send(msg)
            await asyncio.sleep(int(time_interval_seconds))



# Main
client = MyClient(channel_id)
client.run(discord_api_key)

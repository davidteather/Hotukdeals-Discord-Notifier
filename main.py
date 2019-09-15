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
            

    def checkDeals(self, url):
        # Selenium stuff
        options = Options()
        options.headless = False
        driver = webdriver.Firefox(options=options)
        driver.set_window_position(0, 0)
        driver.set_window_size(1920, 1080)

        returnMsgs = []
        newArray = []

        with open('data/usedLinks.txt', 'r') as data:
            usedArray = data.readlines()

        # Gets webpage
        driver.get(url)

        

        deals = driver.find_elements_by_xpath('//article[@data-handler="history"]/div[@class="threadGrid"]/div[@class="threadGrid-headerMeta"]/div[@class="flex boxAlign-ai--all-c boxAlign-jc--all-sb space--b-2"]/div[@class="cept-vote-box vote-box overflow--hidden border border--color-borderGrey bRad--a"]/span')

        
        print(len(deals))
        for index in range(0,len(deals)):
            print(index)
            # '//div[@class="cept-vote-box vote-box overflow--hidden border border--color-borderGrey bRad--a"]/span'
            # '//article[@data-handler="history"]/div[@class="threadGrid"]/div[@class="threadGrid-headerMeta"]/div[@class="flex boxAlign-ai--all-c boxAlign-jc--all-sb space--b-2"]/div[@class="cept-vote-box vote-box overflow--hidden border border--color-borderGrey bRad--a"]/span'
            upvotes = int(driver.find_elements_by_xpath('//article[@data-handler="history"]/div[@class="threadGrid"]/div[@class="threadGrid-headerMeta"]/div[@class="flex boxAlign-ai--all-c boxAlign-jc--all-sb space--b-2"]/div[@class="cept-vote-box vote-box overflow--hidden border border--color-borderGrey bRad--a"]/span')[index].text.strip().replace(" ", "").replace("°", "").replace("\n", ""))
            priceString = driver.find_elements_by_xpath('//span[@class="thread-price text--b vAlign--all-tt cept-tp size--all-l size--fromW3-xl"]')[index].text.strip().replace("£", "")
            url = driver.find_elements_by_xpath('//a[@class="cept-tt thread-link linkPlain thread-title--list"]')[index].get_attribute('href')
            

            if priceString != "FREE":
                price = float(priceString)
            else:
                price = 0

            if min_price <= price <= max_price and min_upvotes <= upvotes <= max_upvotes:
                if url not in usedArray:
                    # Return Message
                    message = url + " Satisfies your deal criteria. It is at " + str(upvotes) + " degrees and costs " + str(priceString)
                    returnMsgs.append(message)
                    usedArray.append(url)
                    newArray.append(newArray)

        print('here')
        with open('data/usedLinks.txt', 'a') as fileObj:
            for line in newArray:
                fileObj.write(line)

        

        driver.quit()

        return returnMsgs

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!add-url'):
            text = message.content
            self.checkUrls.append(text.split("!add-url ")[1])
            await message.channel.send(text.split("!add-url ")[1] + " added to the program.")

        if message.content.startswith('!remove-url'):
            text = message.content.split("!remove-url ")[1]
            self.checkUrls.remove(text)
            await message.channel.send(text + " removed from the program.")


    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(int(channel_id)) # channel ID goes here
        while not self.is_closed():
            for page in range(0,int(pages_to_index)):
                res = self.checkDeals(base_url + "?page=" + str(page))
                if res != []:
                    for msg in res:
                        await channel.send(msg)
            await asyncio.sleep(int(time_interval_seconds))

client = MyClient(channel_id)
client.run(discord_api_key)
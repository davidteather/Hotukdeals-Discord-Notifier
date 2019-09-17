# HotUkDeals-Discord-Notifier

This is a website scraping program designed to scrape [this](https://www.hotukdeals.com/) website. It allows the user to input specific criteria and when the program finds a result that matches the criteria you will be notified on discord.

## Getting Started

The following instructions will help you get you running this software.

### Prerequisites

To install the python requirements please run the command below.

```
pip install pip install beautifulsoup4
```

### Installing

Have python 3.x installed. This was tested with 3.7.3

## Running the program

To run the software you first need to add information into the proxies.txt and settings.json

### **Example of settings.json**
```
{
    "min_upvotes": "500",
    "max_upvotes": "1000",
    "base_url": "https://www.hotukdeals.com",
    "pages_to_index": "10",
    "discord_api_token": "1234567890",
    "min_price": "0",
    "max_price": "500",
    "discord_channel_id": "1234567890",
    "time_interval_seconds": "1800"
}
```

**min_upvotes** - The minimum amount of upvotes / degrees to be notified of.

**max_upvotes** - The maximum amount of upvotes / degrees to be notified of.

**base_url** - The base url to be scanned. Default works fine.

**pages_to_index** - The amount of pages you want to index default is 10.

**discord_api_token** - Your discord API token for your bot. [Here](https://www.writebots.com/discord-bot-token/) is a good article on how to get your bot's api token.

**min_price** - The minimum price of the deal you want to be notified of.

**max_price** - The maximum price of the deal you want to be notified of.

**discord_channel_id** - The discord channel ID you want your bot to be talk in and notify you of. [Here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) is a good article on how you are able to get your discord channel id.

**time_interval_seconds** - The amount of time in seconds that you want to delay after all the pages are scraped. I recommend over 30 minutes. 

### **Example of proxies.txt**
```
1234.1234.1234:1010
```

Each line should be a new proxy with a port, must be able to manage SSL.

### Executing the program

Once you have all of the json files configured as you would like simpily run the command below.

```
python main.py
```

The bot will then notify you on discord when the deals match your criteria.

## Built With

* [Python 3.7](https://www.python.org/) - The language used

## Authors

* **David Teather** - *Initial work* - [davidteather](https://github.com/davidteather)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
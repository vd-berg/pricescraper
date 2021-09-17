# Your private price tracker
Will get the price of a product on a certain URL and 
compare it to previous prices and notify you on changes.

# Installation

## Step 1: Clone, create a venv and install requirements
```
git clone git@github.com:vd-berg/pricescraper.git
python3 -m venv pricescraper/
source pricescraper/bin/activate
cd pricescraper
pip install -r requirements.txt
```

## Step 2: Add your Telegram bot
You can skip this step for first time use or testing purposes.

To add your Telegram bot: 
1. In `config.py` add [your Telegram bot](https://core.telegram.org/bots) 
token and chat id.
2. Change `telegram_bot_enabled` to `True`

## Step 3: Running the script
You can run the script by providing it with a CSS selector and URL like so:

```python
go.py "div.product-price span.price span.js-fprice" "https://www.bergfreunde.nl/patagonia-cap-air-hoody-merino-ondergoed/"
```

### 3.1: Adding it to crontab
This syntax is most useful in a cron job. This way you can set check intervals 
as you like and make sure that if one job fails it doesn't fail others as well.

To open your crontab, use `crontab -e` and add to the bottom. You can add as 
many lines as you like.

To make sure it runs in the python venv created in step 1, use this syntax to 
run a check every hour between 9AM and 9PM and log errors to a log file. 
Adjust for your personal home directory.

```bash
0 9-21 * * * /home/martijn/apps/pricescraper/bin/python /home/martijn/apps/pricescraper/go.py "div.product-price span.price span.js-fprice" "https://www.bergfreunde.nl/patagonia-cap-air-hoody-merino-ondergoed/" > /tmp/pricescraperlog.txt 2>$1
```


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
cp pricescraper.db.template pricescraper.db
cp config.py.template config.py
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
python go.py
```

This should output something like:
```
Ja moi! Pries van "Patagonia Cap Air Hoody" is €105.95 (was €149.95 veurege keer). Most moar eem kiekn op: https://www.bergfreunde.nl/patagonia-cap-air-hoody-merino-ondergoed/
```

### 3.1: Adding your own checks
Open the `config.py` file and add your own checks to the `monitor_sites` list.

### 3.2: Adding it to crontab
This script is most useful in a cron job. This way you can set check intervals
as you like.

To open your crontab, use `crontab -e` and add to the bottom.

To make sure it runs in the python venv created in step 1, use this syntax to
run a check every hour between 9AM and 9PM and log errors to a log file.
Adjust for your personal home directory.

```bash
0 9-21 * * * /home/martijn/apps/pricescraper/bin/python /home/martijn/apps/pricescraper/go.py > /tmp/pricescraperlog.txt 2>$1
```

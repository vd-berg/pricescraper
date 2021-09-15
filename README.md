# Your private price tracker
Will get the price of a product on a certain URL and 
compare it to previous prices and notify you on changes.

# Installation

## Step 1: install requirements
Create a Python3 virtual environment and install requirements. 
From your terminal, `cd` to the folder the `pricescraper` folder
is in (so, not the folder itself). Then:

```
python3 -m venv pricescraper/
source pricescraper/bin/activate
cd pricescraper
pip install -r requirements.txt
```

## Step 2: Add your Telegram bot
You can skip this step for first time use or testing purposes.

To add your Telegram bot: 
1. In `go.py` add [your Telegram bot](https://core.telegram.org/bots) 
token and chat id to `pushToTelegram()` method.
2. Uncomment the `self.pushToTelegram(result)` method in `__init__()`

## Step 3: Adjust notification settings
For first time users, notifications are always sent. Even if the price is
the same or higher than last time. This is not very useful once you got
the script going, so you can adjust this in `comparePriceToLog()` by setting
`notifyHigher` and `notifySame` to `False`. 

## Step 4: Add your URL's and CSS Selectors
At the bottom of the script, you can add trackers. Just add the URL and the
CSS Selector where the script can find the price on the page.

Example:
```python
PriceScraper(
	"span[data-qa='sell_price'] strong", 
	"https://www.bever.nl/p/fjaellraeven-abisko-wool-t-shirt-short-sleeve-AIBEE00046.html?colour=2530"
)
```

## Step 5: Run the script as often as you like
You can now run `python3 go.py` by hand, or call it using a cronjob to do it on set intervals.
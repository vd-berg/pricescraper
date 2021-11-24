from config import *

class PriceScraper:

        def __init__(self, cssSelector, uri):

                # Preload class variables to use in class
                self.cssSelector = cssSelector
                self.url = uri
                self.soup = self.getSoupFromURL(self.url)
                self.db = self.getDB()

                # Get result for given URL and css selector
                result = self.comparePriceToLog()
                if result:
                    print(result)
                    if telegram_bot_enabled:
                        self.pushToTelegram(result)

        def getDB(self):
                """
                Gets the sqlite database object. Requires
                table specified below:

                 CREATE TABLE pricelog (
                        url TEXT(4000) NOT NULL,
                        price INTEGER NOT NULL,
                        time datetime NOT NULL,
                        PRIMARY KEY (url, time)
                 );
                """

                import sqlite3
                import os

                db_path = os.path.abspath('pricescraper.db')
                return sqlite3.connect(db_path)

        def getSoupFromURL(self, url):
                """
                Will convert the source of a given URL
                to a BeautifulSoup object.
                """

                from bs4 import BeautifulSoup
                import urllib.request

                # Get source code for given URL
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'PriceScraperApp/1.0')]
                urllib.request.install_opener(opener)
                fp = urllib.request.urlopen(url)
                mybytes = fp.read()
                htmlsource = mybytes.decode("utf8")

                # Convert to BeautifulSoup object
                soup = BeautifulSoup(htmlsource, 'html.parser')

                # Close connection
                fp.close()

                # Return BeautifulSoup object
                return soup

        def sanitizePrice(self, price) -> float:
                """
                Will try to convert any price string to
                a float variable. Admittedly, quite ugly.
                """

                price = price.replace("€", "")
                price = price.replace(".", "") # Thousand separator
                price = price.replace(",", ".")
                return float(price)

        def getPrice(self) -> float:
                """
                Will try to extract the price from
                the BeautifulSoup object by use of the
                css selector. Will also attempt to convert
                price string to a float variable.
                """

                # Find contents of css selector in BeautifulSoup object
                result = self.soup.select(self.cssSelector)

                # There should be exactly 1 price found
                if len(result) == 1:

                        # Get string value of this css selector
                        priceString = result[0].getText()

                        # Tidy it up and return as float
                        return self.sanitizePrice(priceString)

                else:
                        raise Exception(
                                "{}: Expected to find exactly one result " \
                                "for CSS selector {} but found {}.".format(
                                        self.soup.title.getText(),
                                        self.cssSelector,
                                        str(len(result))
                                )
                        )

        def logPrice(self, currentPrice) -> None:
                """
                Log the current price in the database.
                """

                c = self.db.cursor()
                c.execute("""
                        INSERT INTO `pricelog` (`url`, `price`, `time`)
                        VALUES (?, ?, strftime('%Y-%m-%d %H:%M:%S','now'));
                """, (self.url, currentPrice))
                self.db.commit()

        def comparePriceToLog(self, logAfterCompare = True) -> str:
                """
                Will:
                1. Get the price for the url/cssSelector given in constructor
                2. Compare to average price
                3. Return string for notify message according to settings given
                """

                # Get the current price
                currPrice = self.getPrice()

                # Look up average price for this URL
                c = self.db.cursor()
                c.execute("""
                        SELECT `price`
                        FROM `pricelog`
                        WHERE `url` = ?
                        ORDER BY `time` DESC
                        LIMIT 1;
                """, (self.url,))
                result = c.fetchone()

                # Should we log the new price in the database?
                if logAfterCompare:
                        self.logPrice(currPrice)

                # If we found an average price
                if result:
                        lastKnownPrice = result[0]

                        # Build message
                        response = 'Ja moi! Pries van "%s" is €%g '\
                                '(was €%g veurege keer). '\
                                'Most moar eem kiekn op: %s' % (
                                self.soup.title.getText(),
                                currPrice,
                                lastKnownPrice,
                                self.url
                        )

                        if (notify_price_islower and currPrice < lastKnownPrice)\
                        or (notify_price_ishigher and currPrice > lastKnownPrice)\
                        or (notify_price_isequal and currPrice == lastKnownPrice):
                                return response

        def pushToTelegram(self, message):
                """
                Will push a string to a Telegram bot. Please see
                https://core.telegram.org/bots
                """

                if telegram_bot_token == '' or telegram_bot_chat_id == '':
                        raise Exception('''
                                You need a Telegram bot token and chat_id to
                                send messages to your Telegram bot. Add them
                                to the config.py
                        ''')

                import requests

                request_str = 'https://api.telegram.org/bot{bot_token}'\
                        '/sendMessage?chat_id={chat_id}&parse_mode=Markdown&'\
                        'text={message}'.format(
                                bot_token = telegram_bot_token,
                                chat_id = telegram_bot_chat_id,
                                message = message
                        )

                response = requests.get(request_str)

                return response.json()

# Loop through sites listed in config.py
for site in monitor_sites:
    for site_url in site['urls']:

        # Sites change, we don't want to stop all checks if one fails
        try:
            PriceScraper(site['css_selector'], site_url)
        except Exception as ex:

            msg = 'Check failed for selector "{css}" ' \
            'on "{url}" with Exception {exception}'

            print(msg.format(
                css = site['css_selector'],
                url = site_url,
                exception = ex
            ))
            continue

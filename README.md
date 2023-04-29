# holland2stay_parser
To run this code, you'll need Python installed on your computer, along with the following dependencies:

1. Selenium: `pip install selenium`
2. Requests: `pip install requests`
3. Webdriver Manager: `pip install webdriver-manager`

The code is a Python script that does the following:

1. Reads credentials (bot token and chat ID) from a JSON file called `creds.json` for sending messages via Telegram.
2. Defines a specific price range and a URL for searching available residences on the holland2stay website.
3. Defines filters to exclude specific residences from the search results.
4. Launches a headless Firefox browser with Selenium, navigates to the URL, and scrapes available residences with the specified filters.
5. Sends a Telegram message with the number of available apartments, a random apartment from the list, and the bot's status (whether it's alive and working).
6. The script catches any exceptions and sends error messages via Telegram as well. It also cleans up after itself by closing the browser and removing log files.

To run this script execute the following command in the terminal:

```
python parser.py
```

Make sure you have the `creds.json` file in the same directory as the script with the correct bot token and chat ID.

Please note that this code was created for fun and educational purposes. Be mindful of the websites you scrape and ensure you comply with their terms of service or any applicable usage limitations.

import datetime
import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from random import choice

bot_token = ""
chat_id = ""


def get_current_hour():
    return datetime.datetime.now().hour

def read_last_alive_date():
    if os.path.exists('last_alive.txt'):
        with open('last_alive.txt', 'r') as f:
            return f.read()


def write_last_alive_date(date: str):
    with open('last_alive.txt', 'w') as f:
        f.write(date)


def send_telegram_message(message):
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}')

def get_list_of_residences_texts(driver):
    url = "https://holland2stay.com/residences.html?available_to_book=179"
    driver.get(url)
    items_list = driver.find_element(By.CLASS_NAME, "regi-list")
    items = items_list.find_elements(By.CLASS_NAME, "regi-item") 
    items = [item.text for item in items if "book directly" in item.text.lower()]
    return items


try:
    url = "https://holland2stay.com/residences.html"

    user_agent = "Mozilla/5.0 (X11; Linux i686; rv:104.0) Gecko/20100101 Firefox/104.0"
    options = Options()
    options.add_argument('--headless')
    options.set_preference("general.useragent.override", f"{user_agent}")
    print("Starting Firefox")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    driver.set_page_load_timeout(30)
    print("Firefox started")
    driver.get(url)
    print("Page loaded")
    attribute_value = "available_to_book"
    text = "Available to book"
    print("Searching for element")
    filters_panel = driver.find_element(by=By.CSS_SELECTOR, value=f"div[attribute='{attribute_value}']")
    total_links = len(filters_panel.find_elements(By.TAG_NAME, "a"))
    print(f"Found {total_links} links")
    if text in filters_panel.text or total_links > 2:
        residences_texts = get_list_of_residences_texts(driver)
        send_telegram_message(f"""There are {len(residences_texts)} apartment(s) available to book directly."""
                              f"""\n{url}\nRandom apartment:\n{choice(residences_texts)}""")
    today = str(datetime.datetime.now().date())
    last_alive_date = read_last_alive_date()
    if (get_current_hour() >= 9) and (((last_alive_date is not None) and (last_alive_date < today)) or (last_alive_date is None)):
        send_telegram_message("The bot is alive today")
        write_last_alive_date(today)
except Exception as e:
    send_telegram_message(f"Error: {e}")
finally:
    time.sleep(5)
    try:
        driver.close()
    except Exception as e:
        send_telegram_message(str(e))
    # remove logs
    if os.path.exists("geckodriver.log"):
        os.remove("geckodriver.log")

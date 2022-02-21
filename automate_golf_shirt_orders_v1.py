# Pyautogui for searching the webpage.
import pyautogui

#Selenium imports for website navigation.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import pandas as pd
import numpy as np
import json
import time
import sys


PATH = "C:\Program Files (x86)\chromedriver.exe" #Directory of the Chromedriver
serv = Service(PATH)
chrome_options = Options()
chrome_options.add_argument("--incognito") # Incognito helps avoid ads and sponsored items.
driver = webdriver.Chrome(service=serv, options=chrome_options)

#Navigate to Amazon website.
WEBSITE = "https://www.amazon.com/"
driver.get(WEBSITE)
driver.maximize_window()
web_title = driver.title
print(web_title)

# https://www.amazon.com/s?k=ASIN # Should be the same as typing the ASIN in the search bar.


df_orders = pd.read_excel('shirts_order_form.xlsx')

df_orders = df_orders.sort_values(by=['ASIN']).reset_index(drop=True)

asins_distinct = list(set(df_orders['ASIN']))
num_asins = len(asins_distinct)
print(asins_distinct)
print(f"{num_asins} distinct ASINS found.")

asins_links = list(set(df_orders['Link']))

# Create list of product URLs.
asin_search_urls_list = [f"https://www.amazon.com/s?k={asin}" for asin in asins_distinct]
print(asin_search_urls_list)
print(asins_links)

for link in asins_links:
    driver.get(link)
    time.sleep(5)    
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write('asin')
    time.sleep(5)  



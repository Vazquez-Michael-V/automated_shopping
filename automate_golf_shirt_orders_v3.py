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
#(df_orders.head())

# Create dictionary with keys = asin, value = link.
asins_distinct = list(df_orders['ASIN'].drop_duplicates())
links_distinct = list(df_orders['Link'].drop_duplicates())
asins_links_zip = zip(asins_distinct, links_distinct)
asins_links_dict = {key: value for key, value in asins_links_zip}
print(asins_links_dict)

# Navigate to page and control f for the ASIN.
# Use class and id in version 3. Drop the control f.
# id = detailBullets_feature_div
# class = a-text-bold
item = 1
for asin, link in asins_links_dict.items():    
    print(item)
    driver.get(link)       
    time.sleep(5)
    # asin_check = driver.find_element(By.ID, 'detailBullets_feature_div' ).find_element(By.CLASS_NAME, 'a-text-bold').text
    # a-text-bold appears on the page multiple times.
    item_details = driver.find_element(By.ID, 'detailBullets_feature_div' ).text
    # Create a text file to readlines() from.
    if item == 1:
        with open('shop_text_details.txt', 'w') as f:
            f.write(item_details)
            f.write("\n")
    else:
        with open('shop_text_details.txt', 'a') as f:
            f.write(item_details)
            f.write("\n")
    #item_details = json.decoder(item_details)
    print(item_details)
    print(type(item_details))
    
    time.sleep(5)  
    driver.refresh()
    item +=1

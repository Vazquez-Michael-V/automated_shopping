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

# https://www.amazon.com/s?k= redirects to amazon homepage.

# Note: Amazon uses ASIN for all products except books, which use ISBN.

# Need to check for empty elements.
# Need to .strip() the elements.
df_shopping = pd.read_excel('shopping_file.xlsx')

# Check the ExpectedPrice column.
try:    
    df_shopping['ExpectedPrice'] = pd.to_numeric(df_shopping['ExpectedPrice'])
except ValueError:
    print("Please check excel file. Ensure all entries in ExpectedPrice column are numbers.")
    sys.exit(0)

# Create a dictionary with item names as keys, None values.
item_names = list(df_shopping['ItemNames'])
item_price_dict = {key: None for key in item_names}
asin_list = list(df_shopping['ASIN'])

expected_prices_list = list(df_shopping['ExpectedPrice'])
print(expected_prices_list)

cart_status = []
item_details = []
prices_actual_list = []
notes = []
percent_change_col = []
# Uses item name and ASIN to increase chance of correct item being selected.
price_amount = None
percent_change = None
in_cart_bool = None
note = None
# Need a way to avoid clicking sponsored items.
for number, asin in enumerate(asin_list):
    try: 
        # Search the asin and check if the item link can be found.
        print(asin)        
        product_url = f"https://www.amazon.com/s?k={asin}" # Search the ASIN.
        driver.get(product_url) #Navigate to the webpage.  
        partial_name = item_names[number][:20]        
    # Check if the item link can be found.
        result_to_click = WebDriverWait(driver, 10).until(
               EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, partial_name)))
        result_string = result_to_click.get_attribute('href')  
        
        # Need a way to avoid clicking sponsored items.
        
        # asin should be in the item link.
        if asin in result_string:
            # Try to find the price of the item.
            result_to_click.click() # Navigate to the item's page. 
            asin_in_link_bool = True
        else:
            print("ASIN not in link.")
            price_amount = 0
            percent_change = 0
            in_cart_bool = "No"
            note = "ASIN not in link."
            
            asin_in_link_bool = False   
        print(price_amount)
        print(asin_in_link_bool)
        
        if asin_in_link_bool == True:
            try:
                print("ASIN in link.")                   
                item_info = driver.find_element(By.XPATH, "//div[@class='a-section aok-hidden twister-plus-buying-options-price-data']").get_attribute('innerHTML')  
                item_info = json.loads(item_info)    
                item_details.append(item_info)
                price_amount = item_info[0]['priceAmount']                
                print(price_amount)
            
            # Add more ways to find the price.
            except NoSuchElementException or TimeoutException:
                price_amount = 0
                percent_change = 0
                in_cart_bool = "No"
                note = "Price not found."
                print("Price not found.")
        
        if price_amount != 0:
            acceptable_increase = 0.05
            print(expected_prices_list[number])
            percent_change = ((price_amount - expected_prices_list[number]) / expected_prices_list[number])
            if percent_change <= acceptable_increase:
                in_cart_bool = "Yes"
                note = "Acceptable price change."
            else:
                in_cart_bool = "No"
                note = "Unacceptable price change."
                
        # else:
        #     note = "NA"
    except:        
        print(f"Link not found for {asin}.")
        
        
    # Append variables.
    finally:
        prices_actual_list.append(price_amount)
        percent_change_col.append(percent_change)
        cart_status.append(in_cart_bool)
        notes.append(note)
 
# Add columns to df_shopping.
print(prices_actual_list)
df_shopping['ActualPrices']=prices_actual_list
df_shopping['PercentChange']=percent_change_col
df_shopping['CartStatus']=cart_status
df_shopping['Notes']=notes
print(df_shopping)

#Create excel files of df_shopping.
shopping_filename='shopping_cart_file.xlsx'  
with pd.ExcelWriter(shopping_filename) as writer:       
    df_shopping.to_excel(writer, index=False)
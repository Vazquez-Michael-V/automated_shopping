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

# Create dictionary with keys = asin, value = link.
asins_distinct = list(df_orders['ASIN'].drop_duplicates())
links_distinct = list(df_orders['Link'].drop_duplicates())
asins_links_zip = zip(asins_distinct, links_distinct)
asins_links_dict = {key: value for key, value in asins_links_zip}
#print(asins_links_dict)

# Set up a dictionary to use for navigating the dropdown menus.
# Two drop down menus: Color/Design and Size.
emp_orders = {asin: {} for asin in asins_distinct}
for asin, emp_order_info in emp_orders.items():
    df_dropdown_temp = df_orders.loc[(df_orders['ASIN'] == asin)]
    df_dropdown_temp = df_dropdown_temp.drop(columns = ['Link', 'ExpectedMinPrice', 'ExpectedMaxPrice', 'Brand'])
    df_dropdown_temp = df_dropdown_temp[['EmployeeID', 'ASIN', 'ShirtDesign','ShirtSize']]
    dropdown_design = list(df_dropdown_temp['ShirtDesign'])
    dropdown_size = list(df_dropdown_temp['ShirtSize'])
    dropdown_empid = list(df_dropdown_temp['EmployeeID'])
    emp_orders[asin]['Designs'] = dropdown_design
    emp_orders[asin]['Sizes'] = dropdown_size
    emp_orders[asin]['EmployeeID'] = dropdown_empid
    emp_orders[asin]['Price'] = None
    # print(df_dropdown_temp)
    
# for k, v in emp_orders.items():
#     print(f"{k}\n{v}\n")

orders_text_file = 'shop_text_details.txt'
item = 1
for asin, link in asins_links_dict.items():    
    print(item)
    driver.get(link)       
    time.sleep(5)

    # Get the price of the item here and add it to the text file.
    # Need to select the size and color before the price will display.
    # Need to account for the item not being available.
    # item_price = driver.find_element(By.ID, 'corePriceDisplay_desktop_feature_div')
    
    # Find the shirt color buttons.
    # colors = driver.find_element(By.XPATH, '//*[@id="variation_color_name"]/ul').text
 
    # twisterContainer
    # 'twisterContainer' contains all color and size options in a drop down menu.
    
    
    # Find the colors/designs on the page.
    colors_buttons = driver.find_element(By.ID, 'variation_color_name').find_elements(By.TAG_NAME, 'li')
    print(len(colors_buttons))
    for color in colors_buttons:
        color_string = color.get_attribute('title')        
        color_string = str(color_string)
        print(color_string)
        # color_string_color = str.find(color_string, )
        
        # if color_string in emp_orders[asin]['Designs']:

    item_details = driver.find_element(By.ID, 'detailBullets_feature_div' ).text
    
    if item == 1:
        with open(orders_text_file, 'w') as f:            
            replace_text = f"_{asin}:"
            item_details = item_details.replace(' :', replace_text)
            f.write(item_details)
            f.write("\n")
    else:
        with open('shop_text_details.txt', 'a', encoding='UTF-8') as f:
            replace_text = f"_{asin}:"
            item_details = item_details.replace(' :', replace_text)
            f.write(item_details)
            f.write("\n")
        
    time.sleep(5)  
    driver.refresh()
    item +=1

# Read the text file and create two lists based on the colon delimiter.
details_keys = []
details_values = []
with open(orders_text_file, 'r') as orders_f:
    for line in orders_f:
        delim = str.find(line, ':')
        key_part = line[:delim].strip()
        value_part = line[delim:].replace(': ', '').strip()
        details_keys.append(key_part)
        details_values.append(value_part)


# Create a dictionary to store product details.
asins_dict = {key: None for key in asins_distinct}
# print(asins_dict)
d = {'Keys': details_keys, 'Values': details_values}
df_details = pd.DataFrame(d)
#print(df_details)
for asin in asins_distinct:    
    df_temp = df_details[df_details['Keys'].str.contains(f"{asin}")]
    keys_temp = list(df_temp['Keys'])
    for num, key in enumerate(keys_temp):
        delim = str.find(key, '_')
        new_key = key[:delim]
        keys_temp[num]=new_key
    values_temp = list(df_temp['Values'])
    temp_zip = zip(keys_temp, values_temp)
    temp_dict = {key: value for key, value in temp_zip}
    asins_dict[asin]=temp_dict


# for k, v in asins_dict.items():
#     print(f"{k}\n{v}\n")

# print(asins_dict['B07Q5CHX25'])




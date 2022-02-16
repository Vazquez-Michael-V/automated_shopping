import pandas as pd
import numpy as np

# Suppose have 30 employees attending the golf party.
# Create 30 employee ids.
employees_list = []
for i in range(1,31):
    if i <= 9:
        employees_list.append(f"E00{i}")
    else:
        employees_list.append(f"E0{i}")


# Find some shirt options on Amazon.
yatta_golf_designs = ['The Patriot', 'Primal Forest', 'Subtle Pines']
# yatta link: https://www.amazon.com/YATTA-GOLF-Standout-Performance-Shirts/dp/B095PWKR6L

mier_designs = ['Red02- Long Sleeve', 'Navy01- Short Sleeve', 'Black01- Short Sleeve'] 
# mier link: https://www.amazon.com/MIER-Outdoor-Performance-Tactical-Moisture-Wicking/dp/B087BP5C9K

coofandy_designs = ['Black', 'Grey', 'Blue', 'Red']
# coofandy link: https://www.amazon.com/COOFANDY-Sleeve-Zipper-Fitted-Tshirts/dp/B08Y1FH5HM

under_armour_designs = ['Royal (400)/Graphite', 'Black (001)/Graphite', 'Electric Blue (428)/Pitch Gray', 'Tech Blue (432)/Pitch Gray']
# under armour link: https://www.amazon.com/Under-Armour-Royal-Graphite-Medium/dp/B08LNZXJXN

options_shirts_designs = yatta_golf_designs + mier_designs + coofandy_designs + under_armour_designs
options_shirts_sizes = ['Small', 'Medium', 'Large', 'X-Large', 'XX-Large']

# Randomly generate the shirt picks and the sizes.
employee_shirt_picks = [options_shirts_designs[np.random.randint(0,13)] for i in range(len(employees_list))]
employee_shirt_sizes = [options_shirts_sizes[np.random.randint(0,4)] for i in range(len(employees_list))]

expected_min_price = []
expected_max_price = []
asin_list = []
brand_list = []
link_list = []
for shirt in employee_shirt_picks:
    if shirt in yatta_golf_designs:
        expected_min_price.append(19.32)
        expected_max_price.append(47.98)
        asin_list.append('B098KHG3SY')
        brand_list.append('Yatta Golf')
        link_list.append('https://www.amazon.com/YATTA-GOLF-Standout-Performance-Shirts/dp/B095PWKR6L')
    elif shirt in mier_designs:
        expected_min_price.append(29.99)
        expected_max_price.append(29.99)
        asin_list.append('B087BCP5CX')
        brand_list.append('Mier')
        link_list.append('https://www.amazon.com/MIER-Outdoor-Performance-Tactical-Moisture-Wicking/dp/B087BP5C9K')
    elif shirt in coofandy_designs:
        expected_min_price.append(17.99)
        expected_max_price.append(23.99)
        asin_list.append('B08RS5MBM8')
        brand_list.append('Coofandy')
        link_list.append('https://www.amazon.com/COOFANDY-Sleeve-Zipper-Fitted-Tshirts/dp/B08Y1FH5HM')
    elif shirt in under_armour_designs:
        expected_min_price.append(25.84)
        expected_max_price.append(33.19)
        asin_list.append('B07Q5CHX25')
        brand_list.append('Under Armour')
        link_list.append('https://www.amazon.com/Under-Armour-Royal-Graphite-Medium/dp/B08LNZXJXN')

# print(employees_list)
# print(employee_shirt_picks)

shirts_dict = {'EmployeeID': employees_list, 'ShirtDesign': employee_shirt_picks, 'ShirtSize': employee_shirt_sizes,
               'Brand': brand_list, 'ExpectedMinPrice': expected_min_price, 'ExpectedMaxPrice': expected_max_price, 'ASIN': asin_list,   
               'Link': link_list
               }

df_shirts = pd.DataFrame(data=shirts_dict)
print(df_shirts)

filename = 'shirts_order_form.xlsx'
with pd.ExcelWriter(filename) as writer:
    df_shirts.to_excel(writer, index=False)
    
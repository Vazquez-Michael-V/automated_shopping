# Create a shopping list using Python.

import pandas as pd


shopping_dict = {'ItemNames': ['TurboTax Deluxe 2021 Tax Software, Federal and State Tax Return with Federal E-file [Amazon Exclusive] [PC/Mac Disc]',
                                          
                                          'Microsoft Office Home & Student 2021 | One-time purchase for 1 PC or Mac| Download',
                                          'PDF Extra 2021 - Professional PDF Editor – Edit, Protect, Annotate, Fill and Sign PDFs - 1 Windows PC/1 User/Lifetime license',
                                          'Original HP 67 Black/Tri-color Ink Cartridges (2-pack) | Works with HP DeskJet 1255, 2700, 4100 Series, HP ENVY 6000, 6400 Series | Eligible for Instant Ink | 3YP29AN',
                                          'Pen', 'Notepad', 'Paper Clips','H&R Block Tax Software Deluxe + State 2021 with 3% Refund Bonus Offer (Amazon Exclusive) | [PC Download]',
                                          '8-Piece Insulated Lunch Box Set - Insulated Lunch Bag for Women Men - 6-pc Glass Food Container Set, 3 Glass Containers Leakproof Locking Lids & Ice Pack - 2-Compartment Cooler Tote for Office Work'
                                         
                                         
                                          ],
                 
                  'ASIN': ['B09CHP83J3', 'B09H7GPR1G', 'B08SJGNB2J', 'B08412HXK9', 'B00347A8NK', 'B00WL5PDU4', 'B002MCZA40', '‎B09JG47T44', 'B081TKCW5F'],
                  
                  'ExpectedPrice': [30.25, 110.99, 99.99, 29.89, 5.01, 18.49, 14.99, 29.97, 25.99]
                  }


df_shop = pd.DataFrame(shopping_dict)

filename = 'shopping_file.xlsx'
with pd.ExcelWriter(filename) as writer:
    df_shop.to_excel(writer, index=False)
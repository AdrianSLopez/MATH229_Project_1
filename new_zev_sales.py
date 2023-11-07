import pandas as pd
from datascience import *
import numpy as np
import statistics as s
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('MacOSX')

from collections import OrderedDict
from datetime import datetime

def sort_dict_by_date(the_dict, date_format):
    # Python dicts do not hold their ordering so we need to make it an
    # ordered dict, after sorting.
    return OrderedDict(sorted(
            the_dict.items(),
            key=lambda x: datetime.strptime(x[0], date_format)
        ))

def yearFrom(dates):
    relabeledDates = []

    for date in dates:
        date = date.split('/')
        relabeledDates.append(int(date[2]))
    
    return relabeledDates

def joinDateGasPriceTogether(dates, prices):
    sortedPrices = {}

    for i in range(len(dates)):
        sortedPrices[dates[i]] = prices[i]
    
    return sortedPrices

def uniqueMakes(cars):
    unique_cars = set()

    for car in cars:
        unique_cars.add(car)

    return unique_cars


# ELECTRIC VEHICLE DATA
data_new_zev_sales_LA = Table.read_table('Data/New_ZEV_Sales_Last_updated_10-31-2023_ada_County.csv').where('County', are.equal_to('Los Angeles')).where('FUEL_TYPE', are.equal_to('Electric'))
data_new_zev_sales_LA_all = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'Make', 'MODEL').group(['Data Year'], sum).where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).relabel('Data Year',  'Year').relabel('Number of Vehicles sum', '# of EVs purchased')

make_LA_sales = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'MODEL').where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).group(['Data Year', 'MAKE'], sum)


vehicle_makes = uniqueMakes(make_LA_sales.column('MAKE'))
table_for_every_make1 = []

for make in vehicle_makes:
    table_for_every_make1.append(make_LA_sales.where('MAKE', make).relabel('Number of Vehicles sum', make+' purchased').drop('MAKE'))

# for loop to create table for all vehicle make, then add NA for missing years for each table, then display all in one line graph

table_for_every_make2 = []
for table in table_for_every_make1:
    if len(table.column('Data Year')) != 13:
        years_left = 13- len(table.column(0))
        add_years = []
        add_purchase = []

        for year in range(1, years_left):
            add_years.append(2009+year)

        for p in add_years:
            add_purchase.append(0)

        for year in table.column(0):
            add_years.append(year)

        for purchase in table.column(1):
            add_purchase.append(purchase)

        table_for_every_make2.append(Table().with_columns('Data Year', add_years, table.labels[1], add_purchase))



# CREATE HTML TABLE OF DATA
pre_html = "<!DOCTYPE html>\n <html> \n<head> \n <style> \n .fixTableHead { \n overflow-y: auto;  \n  height: 750px; \n} \n .fixTableHead thead th { \n  position: sticky;     \n   top: 0;     \n }     \n table {     \n   border-collapse: collapse;             \n   width: 100%;     \n }     \n th,    \n  td {     \n   padding: 8px 15px;    \n   border: 2px solid #529432;     \n }    \n th {     \n   background: #ABDD93;     \n } \n   </style> \n </head> \n <body style='text-align: center;'>   \n <h1 style='text-align: center;'>New Electric Vehicles (EVs) purchased in Los Angeles 2010-2022</h1>"
post_html = "\n</body>  \n</html>"
data_html = pre_html #+ "<div class=\"fixTableHead\" >" + make_LA_sales.as_html() + '</div>'

for data in table_for_every_make2:
    data_html += "<div class=\"fixTableHead\" >" + data.as_html() + '</div>'

# WRITE HTML TABLE TO HTML FILE, USE VSC EXTENSION LIVESERVER TO VIEW
try:
    htmlFile = open('view.html', 'w')
    htmlFile.write(data_html)
    htmlFile.close()

    print('HTML code written')
except: 
    print('Error')


# DISPLAY PLOTS USING MacOSX on mac and TkAgg on Windows
print('displaying plot(s)...')
# data_new_zev_sales_LA.scatter('Year', '# of EVs purchased')

plt.title('New Electric Vehicles purchased per year in Los Angeles 2010-2022 ')
plt.grid(color='grey', linestyle = '--', linewidth=0.4)
# plt.show()
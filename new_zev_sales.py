import pandas as pd
from datascience import *
import numpy as np
import statistics as s
import matplotlib
from matplotlib import pyplot as plt
import plotly.express as px

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
    table_for_every_make1.append(make_LA_sales.where('MAKE', make).relabel('Number of Vehicles sum', make).drop('MAKE'))


#  Given an array of continous years between 2010 to 2022, return an array from 2010 to 2022

# get lower number and find missing years between 2010 to lowest year
# get highest year and find missing years between highest year to highest year


table_for_every_make2 = []
# fill in data gaps outside of filled data
for table in table_for_every_make1:
    if len(table.column(0)) != 13:
        pre_years = []
        pre_purchase = []

        for i in range(2010, table.column('Data Year')[0]):
            pre_years.append(i)
            pre_purchase.append(0)

        for i in range(len(table.column(0))):
            pre_years.append(table.column(0)[i])
            pre_purchase.append(table.column(1)[i])

        for post_year in range(table.column(0)[len(table.column(0))-1]+1, 2023):
            pre_years.append(post_year)
            pre_purchase.append(0)
 
        table_for_every_make2.append(Table().with_columns('Data Year', pre_years, table.labels[1], pre_purchase))


# fill in data gaps in between data (Mistubishi, MINI, SMART) 
# CHECKPOINT CHECKPOINT CHECKPOINT CHECKPOINT CHECKPOINT
for table in table_for_every_make2:
    if len(table.column(0)) != 13:
        
        i = 0
        j = i+1

        while j < 12:
            if
        # iterate through years
        # once consecutive years break save start broken year and topbroken year


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
# data_new_zev_sales_LA_all.scatter(data_new_zev_sales_LA_all.labels[0], data_new_zev_sales_LA_all.labels[2])
# print(data_new_zev_sales_LA_all.labels)

# graph error

# print(table_for_every_make2[0].labels)

newFig = px.scatter(table_for_every_make2[0].to_df(), x="Data Year", y=table_for_every_make2[0].labels[1]).update_traces(mode="lines+markers")
# for i in range(1, len(table_for_every_make2)):
#     newFig.add_scatter(table_for_every_make2[i].to_df(),  color=table_for_every_make2[i].labels[1])

newFig.show()
# plt.title('New Electric Vehicles purchased per year in Los Angeles 2010-2022 ')
# plt.grid(color='grey', linestyle = '--', linewidth=0.4)
# plt.show()
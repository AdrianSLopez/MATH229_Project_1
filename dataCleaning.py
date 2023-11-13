from collections import OrderedDict
from datetime import datetime
from datascience import *
import numpy as np

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

def displayHTMLTables(data_tables):
    # CREATE HTML TABLE OF DATA
    pre_html = "<!DOCTYPE html>\n <html> \n<head> \n <style> \n .fixTableHead { \n overflow-y: auto;  \n  height: 750px; \n} \n .fixTableHead thead th { \n  position: sticky;     \n   top: 0;     \n }     \n table {     \n   border-collapse: collapse;             \n   width: 100%;     \n }     \n th,    \n  td {     \n   padding: 8px 15px;    \n   border: 2px solid #529432;     \n }    \n th {     \n   background: #ABDD93;     \n } \n   </style> \n </head> \n <body style='text-align: center;'>   \n <h1 style='text-align: center;'>New Electric Vehicles (EVs) purchased in Los Angeles 2010-2022</h1>"
    post_html = "\n</body>  \n</html>"
    data_html = pre_html

    for data in data_tables:
        data_html += "<div class=\"fixTableHead\" >" + data.as_html() + '</div>'
    
    # WRITE HTML TABLE TO HTML FILE, USE VSC EXTENSION LIVESERVER TO VIEW
    try:
        htmlFile = open('view.html', 'w')
        htmlFile.write(data_html)
        htmlFile.close()

        print('HTML code written')
    except: 
        print('Error')

def createTableForEveryMake(car_data):
    vehicle_makes = uniqueMakes(car_data.column('MAKE'))
    vehicle_make_tables_1 = []

    for make in vehicle_makes:
        vehicle_make_tables_1.append(car_data.where('MAKE', make).relabel('Number of Vehicles sum', make).drop('MAKE'))

    vehicle_make_tables_2 = fillDataGaps(vehicle_make_tables_1)
    return vehicle_make_tables_2

def fillDataGaps(vehicle_tables):
    data_tables = []

    # fill outer year gaps of data 
    for table in vehicle_tables:
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
    
            data_tables.append(Table().with_columns('Data Year', pre_years, table.labels[1], pre_purchase))
        else:
            data_tables.append(table)

    filled_data = []
    for table in data_tables:
        if len(table.column(0)) != 13:
            years = table.column(0)
            sold = table.column(1)

            current_year = years[0]
            breaking_year = years[0]
            i =1

            # fill in gaps
            while len(years) != 13:
                if years[i] != current_year+1:
                    breaking_year = years[i]

                    missing_years = [i for i in range(current_year+1, breaking_year)]
                    years = np.insert(years, i, missing_years)

                    missing_prices = [0 for i in range(0, len(missing_years))]
                    sold = np.insert(sold, i, missing_prices)
                    i-=1
                else:
                    current_year = years[i]
                
                i+=1

            table = Table().with_columns('Data Year', years, table.labels[1], sold) 

        filled_data.append(table)  

    return filled_data 
    

        



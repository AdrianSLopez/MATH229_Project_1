import pandas as pd
from datascience import *
import numpy as np
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

# ELECTRIC VEHICLE DATA
data_ev_raw = Table.read_table('Data/Vehicle_Population_Last_updated_04-28-2023_ada.csv').where('County', are.equal_to("Los Angeles")).drop('Dashboard Fuel Type Group', 'County', 'Make', 'Model').group(['Data Year', 'Fuel Type'], sum).relabel('Data Year', 'Year').relabel('Number of Vehicles sum', '# of vehicles')
data_BEV = data_ev_raw.where('Fuel Type', are.equal_to('Battery Electric (BEV)')).group(['Year', 'Fuel Type'], sum).drop('Fuel Type').relabel('# of vehicles sum', '# of BEV')
data_PHEV = data_ev_raw.where('Fuel Type', are.equal_to('Plug-in Hybrid (PHEV)')).group(['Year', 'Fuel Type'], sum).drop('Fuel Type').relabel('# of vehicles sum', '# of PHEV')
data_FCEV = data_ev_raw.where('Fuel Type', are.equal_to('Fuel Cell (FCEV)')).group(['Year', 'Fuel Type'], sum).drop('Fuel Type').relabel('# of vehicles sum', '# of FCEV')
data_ZEV = data_BEV.join('Year', data_PHEV).join('Year', data_FCEV)
data_ZEV = data_ZEV.with_column('# of ZEV', data_ZEV.column('# of BEV')+data_ZEV.column('# of PHEV')+data_ZEV.column('# of FCEV'))

#GAS PRICES DATA
#GAS PRICES DATA
data_gas_raw = Table.read_table('Data/Weekly_Los_Angeles_Regular_All_Formulations_Retail_Gasoline_Prices.csv')
data_gas_yearly_average = data_gas_raw.relabel('Weekly Los Angeles Regular All Formulations Retail Gasoline Prices Dollars per Gallon', '$ per gallon').with_column('Year', yearFrom(data_gas_raw.column('Week of'))).group('Year', np.mean).drop('Week of mean').move_to_start('Year').where('Year', are.above_or_equal_to(2010)).where('Year', are.below_or_equal_to(2022)).relabel('$ per gallon mean', '$ per gallon average')
sorted_raw_gas_prices = sort_dict_by_date(joinDateGasPriceTogether(data_gas_raw.column('Week of'), data_gas_raw.column('$ per gallon')), '%m/%d/%Y')
table_sorted_raw_gas_prices = Table().with_columns(
    'Date', sorted_raw_gas_prices.keys(),
    '$ per gallon', sorted_raw_gas_prices.values()
)

# JOINED DATA
data_gas_zev = data_ZEV.join('Year', data_gas_yearly_average).move_to_start('$ per gallon average').move_to_start('Year')


# CREATE HTML TABLE OF DATA
pre_html = "<!DOCTYPE html>\n <html> \n<head> \n <style> \n .fixTableHead { \n overflow-y: auto;  \n  height: 750px; \n} \n .fixTableHead thead th { \n  position: sticky;     \n   top: 0;     \n }     \n table {     \n   border-collapse: collapse;             \n   width: 100%;     \n }     \n th,    \n  td {     \n   padding: 8px 15px;    \n   border: 2px solid #529432;     \n }    \n th {     \n   background: #ABDD93;     \n } \n   </style> \n </head> \n <body>   \n <h1 style='text-align: center;'>Los Angeles's Number of Zero Emission Vehicles (ZEV) 2010-2022</h1> <a href='https://www.energy.ca.gov/data-reports/energy-almanac/zero-emission-vehicle-and-infrastructure-statistics/new-zev-sales'> <p style='text-align: center;'> source </p> </a>"
post_html = "\n</body>  \n</html>"
data_html = pre_html + "<div class=\"fixTableHead\">" + data_ZEV.as_html() + '</div>' + "<div class=\"fixTableHead\">" + "<h1 style='text-align: center;'> Los Angeles Gas Prices 2010-2022</h1> <a href='https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMM_EPMR_PTE_Y05LA_DPG&f=W'> <p style='text-align: center;'> source </p> </a>" + data_gas_yearly_average.as_html() + '</div>' + "<div class=\"fixTableHead\">" + data_gas_zev.as_html() + '</div>' + post_html

# WRITE HTML TABLE TO HTML FILE, USE VSC EXTENSION LIVESERVER TO VIEW
try:
    htmlFile = open('view.html', 'w')
    htmlFile.write(data_html)
    htmlFile.close()

    print('HTML code written')
except: 
    print('Error')


# APPLYING STAT FORMULAS
r = np.corrcoef(data_gas_zev.column('$ per gallon average'), data_gas_zev.column('# of ZEV'))[0, 1]


# DISPLAY PLOTS USING MacOSX on mac and TkAgg on Windows
print('displaying plot(s)...')
data_BEV.scatter('Year', '# of BEV')
# data_FCEV.scatter('Year', '# of FCEV')
# data_PHEV.scatter('Year', '# of PHEV')
# data_ZEV.scatter('Year', '# of ZEV')
# data_gas_yearly_average.scatter('Year', '$ per gallon average')

# table_sorted_raw_gas_prices.scatter('Date', '$ per gallon')

# data_gas_zev.scatter('$ per gallon average', '# of BEV')
# data_gas_zev.scatter('$ per gallon average', '# of FCEV')
# data_gas_zev.scatter('$ per gallon average', '# of PHEV')
# data_gas_zev.scatter('$ per gallon average', '# of ZEV')

plt.title('Battery Electric Vehicles (BEVs) per year (2010-2022)')
plt.grid(color='grey', linestyle = '--', linewidth=0.4)
plt.show()
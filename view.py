import pandas as pd
from datascience import *
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')

def yearFrom(dates):
    relabeledDates = []

    for date in dates:
        date = date.split('/')
        relabeledDates.append(int(date[2]))
    
    return relabeledDates

# ELECTRIC VEHICLE DATA
data_ev_raw = Table.read_table('Data/Vehicle_Population_Last_updated_04-28-2023_ada.csv')
data_ev_raw = data_ev_raw.where('County', are.equal_to("Los Angeles")).drop('Dashboard Fuel Type Group', 'County', 'Make', 'Model').group(['Data Year', 'Fuel Type'], sum)
data_BEV = data_ev_raw.where('Fuel Type', are.equal_to('Battery Electric (BEV)')).group(['Data Year', 'Fuel Type'], sum)
data_PHEV = data_ev_raw.where('Fuel Type', are.equal_to('Plug-in Hybrid (PHEV)')).group(['Data Year', 'Fuel Type'], sum)
data_FCEV = data_ev_raw.where('Fuel Type', are.equal_to('Fuel Cell (FCEV)')).group(['Data Year', 'Fuel Type'], sum)
data_ZEV = data_BEV.join('Data Year', data_PHEV).join('Data Year', data_FCEV).drop('Fuel Type', 'Fuel Type_2', 'Fuel Type_3').relabel('Number of Vehicles sum sum', '# of BEVs').relabel('Number of Vehicles sum sum_2', '# of PHEVs').relabel('Number of Vehicles sum sum_3', '# of FCEVs')
data_ZEV = data_ZEV.with_column('Total # of Zero Emission Vehicles (ZEVs) per year', data_ZEV.column('# of BEVs')+data_ZEV.column('# of PHEVs')+data_ZEV.column('# of FCEVs'))

#GAS PRICES DATA
data_gas_raw = Table.read_table('Data/Weekly_Los_Angeles_Regular_All_Formulations_Retail_Gasoline_Prices.csv')
data_gas_yearly_average = data_gas_raw.relabel('Weekly Los Angeles Regular All Formulations Retail Gasoline Prices Dollars per Gallon', 'Gas Price').with_column('Year', yearFrom(data_gas_raw.column('Week of'))).group('Year', np.mean).drop('Week of mean').move_to_start('Year').where('Year', are.above_or_equal_to(2010)).where('Year', are.below_or_equal_to(2022))

# create html version of data
pre_html = "<!DOCTYPE html>\n <html> \n<head> \n <style> \n .fixTableHead { \n overflow-y: auto;  \n  height: 750px; \n} \n .fixTableHead thead th { \n  position: sticky;     \n   top: 0;     \n }     \n table {     \n   border-collapse: collapse;             \n   width: 100%;     \n }     \n th,    \n  td {     \n   padding: 8px 15px;    \n   border: 2px solid #529432;     \n }    \n th {     \n   background: #ABDD93;     \n } \n   </style> \n </head> \n <body>   \n <h1 style='text-align: center;'>Los Angeles's Number of Zero Emission Vehicles (ZEV) 2010-2022</h1> <a href='https://www.energy.ca.gov/data-reports/energy-almanac/zero-emission-vehicle-and-infrastructure-statistics/new-zev-sales'> <p style='text-align: center;'> source </p> </a>"
post_html = "\n</body>  \n</html>"
data_html = pre_html + "<div class=\"fixTableHead\">" + data_ZEV.as_html() + '</div>' + "<div class=\"fixTableHead\">" + "<h1 style='text-align: center;'> Los Angeles Gas Prices 2010-2022</h1> <a href='https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMM_EPMR_PTE_Y05LA_DPG&f=W'> <p style='text-align: center;'> source </p> </a>" + data_gas_yearly_average.as_html() + '</div>' + post_html

# write data in html format to html file
# use liveserver extension in VSC to view the html file in the browser
try:
    htmlFile = open('view.html', 'w')
    htmlFile.write(data_html)
    htmlFile.close()

    print('HTML code written')
except: 
    print('Error')

# Display plots for BEVs, PHEVS, FCEVs, and Total of ZEVs using matplotlib w/ MacOSX
print('displaying plots...')
# plt.scatter(data_ZEV.column('Data Year'), data_ZEV.column('Total # of Zero Emission Vehicles (ZEVs) per year'))
# plt.xlabel('Year')
# plt.ylabel('Zero Emission Vehicle(s)')
# plt.title('Number of ZEV per year')

plt.scatter(data_gas_yearly_average.column('Year'), data_gas_yearly_average.column('Gas Price mean'))
plt.title('Gas Price Per Year')
plt.xlabel('Year')
plt.ylabel('$ Gas Price')
plt.show()
import pandas as pd
from datascience import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('MacOSX')

data = Table.read_table('Data/Vehicle_Population_Last_updated_04-28-2023_ada.csv')
data = data.where('County', are.equal_to("Los Angeles")).drop('Dashboard Fuel Type Group', 'County', 'Make', 'Model').group(['Data Year', 'Fuel Type'], sum)

data_BEV = data.where('Fuel Type', are.equal_to('Battery Electric (BEV)')).group(['Data Year', 'Fuel Type'], sum)
data_PHEV = data.where('Fuel Type', are.equal_to('Plug-in Hybrid (PHEV)')).group(['Data Year', 'Fuel Type'], sum)
data_FCEV = data.where('Fuel Type', are.equal_to('Fuel Cell (FCEV)')).group(['Data Year', 'Fuel Type'], sum)
data_ZEV = data_BEV.join('Data Year', data_PHEV).join('Data Year', data_FCEV).drop('Fuel Type', 'Fuel Type_2', 'Fuel Type_3')
data_ZEV.relabel('Number of Vehicles sum sum', '# of BEVs').relabel('Number of Vehicles sum sum_2', '# of PHEVs').relabel('Number of Vehicles sum sum_3', '# of FCEVs')
data_ZEV = data_ZEV.with_column('Total # of Zero Emission Vehicles (ZEVs)', data_ZEV.column('# of BEVs')+data_ZEV.column('# of PHEVs')+data_ZEV.column('# of FCEVs'))

# create html version of data
pre_html = "<!DOCTYPE html>\n <html> \n<head> \n <style> \n .fixTableHead { \n overflow-y: auto;  \n  height: 750px; \n} \n .fixTableHead thead th { \n  position: sticky;     \n   top: 0;     \n }     \n table {     \n   border-collapse: collapse;             \n   width: 100%;     \n }     \n th,    \n  td {     \n   padding: 8px 15px;    \n   border: 2px solid #529432;     \n }    \n th {     \n   background: #ABDD93;     \n } \n   </style> \n </head> \n <body>   \n <h1 style='text-align: center;'>Los Angeles's Number of Zero Emission Vehicles (ZEV) 2010-2022</h1> <a href='https://www.energy.ca.gov/data-reports/energy-almanac/zero-emission-vehicle-and-infrastructure-statistics/new-zev-sales'> <p style='text-align: center;'> source </p> </a>"
post_html = "\n</body>  \n</html>"
data_html = pre_html + "<div class=\"fixTableHead\">" + data_ZEV.as_html() +  "</div>"+  "<div class=\"fixTableHead\">" + data.as_html() +  "</div>" + post_html

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
data_ZEV.plot('Data Year', '# of BEVs')
data_ZEV.plot('Data Year', '# of PHEVs')
data_ZEV.plot('Data Year', '# of FCEVs')
data_ZEV.plot('Data Year', 'Total # of Zero Emission Vehicles (ZEVs)')
plt.show()
import pandas as pd
from datascience import *

# df = pd.read_csv('Data/Alzheimer_s_Disease_and_Healthy_Aging_Data.csv')
# df = pd.read_csv('Data/Death_rates_for_suicide__by_sex__race__Hispanic_origin__and_age__United_States.csv')
# print(df.to_string())




data = Table.read_table('Data/Death_rates_for_suicide__by_sex__race__Hispanic_origin__and_age__United_States.csv')
data = data.select('YEAR', 'STUB_LABEL', 'AGE', 'UNIT', 'ESTIMATE')

# create html version of data
pre_html = "<!DOCTYPE html>\n <html> \n<head> \n <style> \n .fixTableHead { \n overflow-y: auto;  \n  height: 750px; \n} \n .fixTableHead thead th { \n  position: sticky;     \n   top: 0;     \n }     \n table {     \n   border-collapse: collapse;             \n   width: 100%;     \n }     \n th,    \n  td {     \n   padding: 8px 15px;    \n   border: 2px solid #529432;     \n }    \n th {     \n   background: #ABDD93;     \n } \n   </style> \n </head> \n <body>   \n <div class=\"fixTableHead\">"
post_html = "</div> \n</body>  \n</html>"
data_html = pre_html + data.as_html() + post_html




# write data in html format to html file
try:
    htmlFile = open('view.html', 'w')
    htmlFile.write(data_html)
    htmlFile.close()

    print('HTML code written')
except: 
    print('Error')


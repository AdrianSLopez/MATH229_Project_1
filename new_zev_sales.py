import pandas as pd
from datascience import *
import numpy as np
import statistics as s
import matplotlib
from matplotlib import pyplot as plt
import plotly.express as px

matplotlib.use('MacOSX')
from dataCleaning import *

# ELECTRIC VEHICLE DATA
data_new_zev_sales_LA = Table.read_table('Data/New_ZEV_Sales_Last_updated_10-31-2023_ada_County.csv').where('County', are.equal_to('Los Angeles')).where('FUEL_TYPE', are.equal_to('Electric'))
data_new_zev_sales_LA_all = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'Make', 'MODEL').group(['Data Year'], sum).where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).relabel('Data Year',  'Year').relabel('Number of Vehicles sum', '# of EVs purchased')
vehicle_make_sales_LA = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'MODEL').where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).group(['Data Year', 'MAKE'], sum)
vehicle_make_sales_LA_tables = createTableForEveryMake(vehicle_make_sales_LA)

displayHTMLTables(vehicle_make_sales_LA_tables)

# DISPLAY PLOTS USING MacOSX on mac and TkAgg on Windows
print('displaying plot(s)...')
# data_new_zev_sales_LA_all.scatter(data_new_zev_sales_LA_all.labels[0], data_new_zev_sales_LA_all.labels[2])
# print(data_new_zev_sales_LA_all.labels)


# display data for every vehicle make
vehicle_make_sold_graph_1 = px.scatter(vehicle_make_sales_LA_tables[0].to_df(), x="Data Year", y=vehicle_make_sales_LA_tables[0].labels[1], name=vehicle_make_sales_LA_tables[0].labels[1]).update_traces(mode="lines+markers")

for i in range(1, int(len(vehicle_make_sales_LA_tables)/2)):
    if vehicle_make_sales_LA_tables[i].labels[1] == 'Tesla': continue
    vehicle_make_sold_graph_1.add_scatter(x=vehicle_make_sales_LA_tables[i].column(0), y=vehicle_make_sales_LA_tables[i].column(1), name=vehicle_make_sales_LA_tables[i].labels[1])

vehicle_make_sold_graph_1.update_layout(
    title="New cars sold per year",
    xaxis_title="Data Year",
    yaxis_title="New Vehicle(s) sold",
    legend_title="Vehicle makes"
)
vehicle_make_sold_graph_1.show()

vehicle_make_sold_graph_2 = px.scatter(vehicle_make_sales_LA_tables[int(len(vehicle_make_sales_LA_tables)/2)].to_df(), x="Data Year", y=vehicle_make_sales_LA_tables[int(len(vehicle_make_sales_LA_tables)/2)].labels[1], name=vehicle_make_sales_LA_tables[int(len(vehicle_make_sales_LA_tables)/2)].labels[1]).update_traces(mode="lines+markers")

for i in range(int(len(vehicle_make_sales_LA_tables)/2) +1, len(vehicle_make_sales_LA_tables)):
    if vehicle_make_sales_LA_tables[i].labels[1] == 'Tesla': continue
    vehicle_make_sold_graph_2.add_scatter(x=vehicle_make_sales_LA_tables[i].column(0), y=vehicle_make_sales_LA_tables[i].column(1), name=vehicle_make_sales_LA_tables[i].labels[1])

vehicle_make_sold_graph_2.update_layout(
    title="New cars sold per year",
    xaxis_title="Data Year",
    yaxis_title="New Vehicle(s) sold",
    legend_title="Vehicle makes"
)
vehicle_make_sold_graph_2.show()
# plt.title('New Electric Vehicles purchased per year in Los Angeles 2010-2022 ')
# plt.grid(color='grey', linestyle = '--', linewidth=0.4)
# plt.show()
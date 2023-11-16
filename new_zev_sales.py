import pandas as pd
from datascience import *
import numpy as np
import statistics as s
import matplotlib
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

matplotlib.use('MacOSX')
from dataCleaning import *

# ELECTRIC VEHICLE DATA
data_new_zev_sales_LA = Table.read_table('Data/New_ZEV_Sales_Last_updated_10-31-2023_ada_County.csv').where('County', are.equal_to('Los Angeles')).where('FUEL_TYPE', are.equal_to('Electric'))
LA_ev_total_sales_per_year_table = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'MAKE', 'MODEL').group(['Data Year'], sum).where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).relabel('Data Year',  'Year').relabel('Number of Vehicles sum', 'Total # of new EVs sold')
LA_total_ev_sold = Table().with_column('Total EV sold between 2010-22', sum(LA_ev_total_sales_per_year_table.column(1)))

LA_ev_sales_per_year_by_make_table = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'MODEL').where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).group(['Data Year', 'MAKE'], sum)
LA_ev_total_sales_per_year_by_make_tables = createTableForEveryMake(LA_ev_sales_per_year_by_make_table)

LA_ev_total_sold_by_make_tables = [Table().with_columns('Make', table.labels[1], 'Total sold', sum(table.column(1))) for table in LA_ev_total_sales_per_year_by_make_tables]
LA_ev_total_sold_by_make_table = Table().with_columns('Make', [table.column(0)[0] for table in LA_ev_total_sold_by_make_tables], 'Total sold', [table.column(1)[0] for table in LA_ev_total_sold_by_make_tables]).sort('Total sold', descending=True) 
LA_ev_total_sold_by_make_table = Table().with_columns(LA_ev_total_sold_by_make_table.labels[0], LA_ev_total_sold_by_make_table.column(0), LA_ev_total_sold_by_make_table.labels[1], LA_ev_total_sold_by_make_table.column(1), 'Relative Frequency', LA_ev_total_sold_by_make_table.column(1)/LA_total_ev_sold.column(0)[0])
LA_ev_total_sold_by_make_percents = [f"{prop:.2%}" for prop in LA_ev_total_sold_by_make_table.column(2)]
LA_ev_total_sold_by_make_table = Table().with_columns(LA_ev_total_sold_by_make_table.labels[0], LA_ev_total_sold_by_make_table.column(0), LA_ev_total_sold_by_make_table.labels[1], LA_ev_total_sold_by_make_table.column(1), 'Relative Frequency', LA_ev_total_sold_by_make_percents)
LA_total_make_sold = Table().with_column('Total sold', sum(LA_ev_total_sold_by_make_table.column(1)))

displayHTMLTables([LA_ev_total_sales_per_year_table, LA_total_ev_sold, LA_ev_total_sold_by_make_table, LA_total_make_sold] + LA_ev_total_sales_per_year_by_make_tables)



# DISPLAY PLOTS USING MacOSX on mac and TkAgg on Windows
print('displaying plot(s)...')
data_new_zev_sales_LA_all_graph = px.scatter(LA_ev_total_sales_per_year_table.to_df(), x="Year", y=LA_ev_total_sales_per_year_table.labels[1]).update_traces(mode="lines+markers")
data_new_zev_sales_LA_all_graph.update_layout(
    title="Figure 1. New electric vehicles (EVs) sold per year",
    title_x=0.5,
    xaxis_title="Year",
    yaxis_title="EV sold",
    font=dict(
    size=22
    )
)
# data_new_zev_sales_LA_all_graph.show()

LA_ev_make_sold_rel_freq_pie = px.pie(LA_ev_total_sold_by_make_table.to_df(), values='Total sold', names='Make', title= str(LA_total_ev_sold.column(0)[0])+' electric vehicles sold between 2010-22').update_traces(textinfo='percent')
# LA_ev_make_sold_rel-freq_pie.show()



vehicle_make_sold_graph_1 = px.scatter()
for i in range(0, int(len(LA_ev_total_sales_per_year_by_make_tables)/2)):
    if LA_ev_total_sales_per_year_by_make_tables[i].labels[1] == 'Tesla': continue
    vehicle_make_sold_graph_1.add_scatter(x=LA_ev_total_sales_per_year_by_make_tables[i].column(0), y=LA_ev_total_sales_per_year_by_make_tables[i].column(1), name=LA_ev_total_sales_per_year_by_make_tables[i].labels[1])
    vehicle_make_sold_graph_1.update_layout(
        title="New electric vehicles (EV) sold per year graph 1",
        xaxis_title="Year",
        yaxis_title="New Vehicle(s) sold",
        legend_title="Vehicle makes"
    )
# vehicle_make_sold_graph_1.show()

vehicle_make_sold_graph_2 = px.scatter()
for i in range(int(len(LA_ev_total_sales_per_year_by_make_tables)/2), len(LA_ev_total_sales_per_year_by_make_tables)):
    if LA_ev_total_sales_per_year_by_make_tables[i].labels[1] == 'Tesla': continue
    vehicle_make_sold_graph_2.add_scatter(x=LA_ev_total_sales_per_year_by_make_tables[i].column(0), y=LA_ev_total_sales_per_year_by_make_tables[i].column(1), name=LA_ev_total_sales_per_year_by_make_tables[i].labels[1])
    vehicle_make_sold_graph_2.update_layout(
        title="New electric vehicles (EV) sold per year graph 2",
        xaxis_title="Year",
        yaxis_title="New Vehicle(s) sold",
        legend_title="Vehicle makes"
    )
# vehicle_make_sold_graph_2.show()


tesla_sold_graph = px.scatter()
for table in LA_ev_total_sales_per_year_by_make_tables:
    if table.labels[1] == 'Tesla':
        tesla_sold_graph.add_scatter(x=table.column(0), y=table.column(1))
tesla_sold_graph.update_layout(
    title="Tesla(s) sold per year",
    xaxis_title="Year",
    yaxis_title="Sold",
    font=dict(
    family="Courier New, monospace",
    size=18,
    color="RebeccaPurple"
    )
)
# tesla_sold_graph.show()

print('DISPLAYING TABLES....')
#  go.Figure(data=[go.Table(
#   header=dict(
#     values=['<b>Column A</b>', '<b>Column B</b>', '<b>Column C</b>'],
#     line_color='white', fill_color='white',
#     align='center',font=dict(color='black', size=12)
#   ),
table1_data =LA_ev_total_sales_per_year_table.to_df()
table1 = go.Figure(data=[go.Table(
    header=dict(values=list(table1_data.columns),
                fill_color='paleturquoise',
                align='center',
                font=dict(
                   size=12
                )),
    cells=dict(values=[table1_data.loc[:, ['Year']], table1_data.loc[:, ['Total # of new EVs sold']]],
               fill_color='lavender',
               align='center',
               font=dict(
                   size = 12
               )))
])
table1.update_layout(title_text='Table 1. New electric vehicles (EVs) sold per year', title_x=0.5, width=750, font=dict(
    size=11
    ))

table1.show()

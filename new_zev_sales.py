import pandas as pd
from datascience import *
import numpy as np
import statistics as s
import matplotlib
from matplotlib import pyplot as plt
import plotly.express as px

matplotlib.use('TkAgg')
from dataCleaning import *

# ELECTRIC VEHICLE DATA
data_new_zev_sales_LA = Table.read_table('Data/New_ZEV_Sales_Last_updated_10-31-2023_ada_County.csv').where('County', are.equal_to('Los Angeles')).where('FUEL_TYPE', are.equal_to('Electric'))
LA_ev_total_sales_per_year_table = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'MAKE', 'MODEL').group(['Data Year'], sum).where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).relabel('Data Year',  'Year').relabel('Number of Vehicles sum', 'Total # of new EVs purchased')
LA_total_ev_sold = Table().with_column('Total EV sold between 2010-22', sum(LA_ev_total_sales_per_year_table.column(1)))

LA_ev_sales_per_year_by_make_table = data_new_zev_sales_LA.drop('County', 'FUEL_TYPE', 'MODEL').where('Data Year', are.above_or_equal_to(2010)).where('Data Year', are.below_or_equal_to(2022)).group(['Data Year', 'MAKE'], sum)
LA_ev_total_sales_per_year_by_make_tables = createTableForEveryMake(LA_ev_sales_per_year_by_make_table)

LA_ev_total_sold_by_make_tables = [Table().with_columns('Make', table.labels[1], 'Total sold', sum(table.column(1))) for table in LA_ev_total_sales_per_year_by_make_tables]
LA_ev_total_sold_by_make_table = Table().with_columns('Make', [table.column(0)[0] for table in LA_ev_total_sold_by_make_tables], 'Total sold', [table.column(1)[0] for table in LA_ev_total_sold_by_make_tables]).sort('Total sold', descending=True)
LA_total_make_sold = Table().with_column('Total sold', sum(LA_ev_total_sold_by_make_table.column(1)))


displayHTMLTables([LA_ev_total_sales_per_year_table, LA_total_ev_sold, LA_ev_total_sold_by_make_table, LA_total_make_sold] + LA_ev_total_sales_per_year_by_make_tables)



# DISPLAY PLOTS USING MacOSX on mac and TkAgg on Windows
print('displaying plot(s)...')
data_new_zev_sales_LA_all_graph = px.scatter(LA_ev_total_sales_per_year_table.to_df(), x="Year", y=LA_ev_total_sales_per_year_table.labels[1]).update_traces(mode="lines+markers")
data_new_zev_sales_LA_all_graph.update_layout(
    title="New electric vehicles (EV) sold per year",
    xaxis_title="Year",
    yaxis_title="EV sold"
)
# data_new_zev_sales_LA_all_graph.show()

LA_ev_make_sold_rel_freq_pie = px.pie(LA_ev_total_sold_by_make_table.to_df(), values='Total sold', names='Make', title='Electric vehicles sold between 2010-22').update_traces(textposition='inside', textinfo='percent+label').update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
LA_ev_make_sold_rel_freq_pie.show()

vehicle_make_sold_graph_1 = px.scatter()
for i in range(0, int(len(LA_ev_total_sales_per_year_by_make_tables)/2)):
    if LA_ev_total_sales_per_year_by_make_tables[i].labels[1] == 'Tesla': continue
    vehicle_make_sold_graph_1.add_scatter(x=LA_ev_total_sales_per_year_by_make_tables[i].column(0), y=LA_ev_total_sales_per_year_by_make_tables[i].column(1), name=LA_ev_total_sales_per_year_by_make_tables[i].labels[1])
    vehicle_make_sold_graph_1.update_layout(
        title="New electric vehicles (EV) sold per year",
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
        title="New electric vehicles (EV) sold per year",
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


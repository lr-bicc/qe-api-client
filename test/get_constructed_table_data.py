from qe_api_client.engine import QixEngine
import math
import pandas as pd


url = 'ws://localhost:4848/app'
qixe = QixEngine(url)
opened_app = qixe.ega.open_doc("Test")
# print(opened_app)
app_handle = qixe.get_handle(opened_app)
# print(app_handle)

list_of_dimensions = ["Alpha"]
# list_of_dimensions = ["Dim1", "Dim2"]
list_of_master_dimensions = ["BjKvssq", "48a5672b-e9b3-4f96-8ff4-480f606e3c14"]
# list_of_measures = ["Sum(Expression1)", "Sum(Expression2)"]
list_of_measures = ["Sum(Expression3)"]
list_of_master_measures = ["snmpR", "1ad7060c-56ec-46d1-b83a-ff1393e0b236"]


df = qixe.get_constructed_table_data(app_handle, list_of_dimensions, list_of_measures, list_of_master_dimensions, list_of_master_measures)

#
# nx_info = qixe.structs.nx_info("table")
# print(nx_info)
#
# hc_dim = []
# for dimension in list_of_dimensions:
#     hc_inline_dim_def = qixe.structs.nx_inline_dimension_def([dimension])
#     hc_dim.append(qixe.structs.nx_dimension("", hc_inline_dim_def))
# for dimension in list_of_master_dimensions:
#     hc_dim.append(qixe.structs.nx_dimension(dimension))
# print(hc_dim)
#
# hc_mes = []
# for measure in list_of_measures:
#     hc_inline_mes = qixe.structs.nx_inline_measure_def(measure)
#     hc_mes.append(qixe.structs.nx_measure("", hc_inline_mes))
# for measure in list_of_master_measures:
#     hc_mes.append(qixe.structs.nx_measure(measure))
# print(hc_mes)
#
#
# hc_def = qixe.structs.hypercube_def("$", hc_dim, hc_mes)
# print("Hypercube Definition:", hc_def)
#
# gen_obj_props = qixe.structs.generic_object_properties(nx_info, "qHyperCubeDef", hc_def)
# print("Generic Object Properties:", gen_obj_props)
#
# hc_obj = qixe.eaa.create_session_object(app_handle, gen_obj_props)
# print(hc_obj)
#
#
# # Get object handle
# hc_obj_handle = qixe.get_handle(hc_obj)
#
# # Get object layout
# hc_obj_layout = qixe.egoa.get_layout(hc_obj_handle)
# print(hc_obj_layout)
#
# # Determine the number of the columns and the rows the table has and splits in certain circumstances the table calls
# no_of_columns = hc_obj_layout['qHyperCube']['qSize']['qcx']
# width = no_of_columns
# no_of_rows = hc_obj_layout['qHyperCube']['qSize']['qcy']
# height = int(math.floor(10000 / no_of_columns))
#
# # Extract the dimension and measure titles and concat them to column names.
# dimension_titles = [dim['qFallbackTitle'] for dim in hc_obj_layout['qHyperCube']['qDimensionInfo']]
# measure_titles = [measure['qFallbackTitle'] for measure in hc_obj_layout['qHyperCube']['qMeasureInfo']]
# column_names = dimension_titles + measure_titles
#
# # Paging variables
# page = 0
# data_values = []
#
# # Retrieves the hypercube data in a loop (because of limitation from 10.000 cells per call)
# while no_of_rows > page * height:
#     nx_page = qixe.structs.nx_page(0, page * height, width, height)
#     hc_data = qixe.egoa.get_hypercube_data(hc_obj_handle, '/qHyperCubeDef', nx_page)['qDataPages'][0]['qMatrix']
#     data_values.extend(hc_data)
#     page += 1
#
# # Creates Dataframe from the content of the attribute 'qText'.
# df = pd.DataFrame([[d['qText'] for d in sublist] for sublist in data_values])
#
# # Assign titles zu Dataframe columns
# df.columns = column_names

print(df)


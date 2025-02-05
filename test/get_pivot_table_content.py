from qe_api_client.engine import QixEngine
import math
import pandas as pd

from test.get_table_content import hc_list

url = 'ws://localhost:4848/app'
qixe = QixEngine(url=url)

# App ID holen
# doc_id = "f9e79d92-652b-4ba8-8487-84e2825b71c5"     # Sales KPI
doc_id = "Test.qvf"

# App öffnen
opened_doc = qixe.ega.open_doc(doc_id)
# print(opened_doc)

doc_handle = qixe.get_handle(opened_doc)

obj = qixe.eaa.get_object(doc_handle, "wPSYmr")     # upyRTm

obj_handle = qixe.get_handle(obj)

obj_layout = qixe.egoa.get_layout(obj_handle)
print(obj_layout)


#
#
# no_of_columns = obj_layout["qHyperCube"]["qSize"]["qcx"]
# print(no_of_columns)
# width = no_of_columns
# no_of_rows = obj_layout["qHyperCube"]["qSize"]["qcy"]
# print(no_of_rows)
# height = int(math.floor(10000 / no_of_columns))
# # height = 1
#
# # Funktion zur Verarbeitung von Knoten, um alle Dimensionen abzurufen
# def get_all_dimensions(node):
#     dimensions = [node['qText']]
#     # if 'qSubNodes' in node and node['qSubNodes']:
#     if node['qSubNodes']:
#         sub_dimensions = []
#         for sub_node in node['qSubNodes']:
#             sub_dimensions.extend([dimensions + d for d in get_all_dimensions(sub_node)])
#         return sub_dimensions
#     else:
#         return [dimensions]
#
# # # Verarbeiten der Zeilenüberschriften (qLeft)
# # row_headers = []
# # for left_node in hc_data['qDataPages'][0]['qLeft']:
# #     row_headers.extend(get_all_dimensions(left_node))
# #
# # Verarbeiten der Spaltenüberschriften (qTop)
# col_headers = []
# nx_page_top = qixe.structs.nx_page(0, 0, width, 1)
# hc_top = qixe.egoa.get_hypercube_pivot_data(obj_handle, "/qHyperCubeDef", [nx_page_top])['qDataPages'][0]['qTop']
# for top_node in hc_top:
#     col_headers.extend(get_all_dimensions(top_node))
#
# # # Verarbeiten der Daten (qData)
# # data_values = []
# # for row in hc_data['qDataPages'][0]['qData']:
# #     data_values.append([cell['qText'] for cell in row])
#
# page = 0
# row_headers = []
# data_values = []
#
# while no_of_rows > page * height:
#     nx_page = qixe.structs.nx_page(0, page * height, width, height)
#
#     hc_left = qixe.egoa.get_hypercube_pivot_data(obj_handle, "/qHyperCubeDef", [nx_page])['qDataPages'][0]['qLeft']
#     for left_node in hc_left:
#         row_headers.extend(get_all_dimensions(left_node))
#
#     hc_data = qixe.egoa.get_hypercube_pivot_data(obj_handle, "/qHyperCubeDef", [nx_page])['qDataPages'][0]['qData']
#     print(hc_data)
#     for row in hc_data:
#         data_values.append([cell['qText'] for cell in row])
#
#     page += 1
#
#
# # Erstellen eines MultiIndex für die Zeilen und Spalten
# row_index = pd.MultiIndex.from_tuples(row_headers)
# col_index = pd.MultiIndex.from_tuples(col_headers)
#
# # Erstellen des DataFrames
# df = pd.DataFrame(data_values, index=row_index, columns=col_index)
#
# # Ergebnis anzeigen
# print(df)
#

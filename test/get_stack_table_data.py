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

obj = qixe.eaa.get_object(doc_handle, "LapHp")     # Stacked bar chart: LapHp | Pie chart: gYyUxS

obj_handle = qixe.get_handle(obj)

obj_layout = qixe.egoa.get_layout(obj_handle)
# print(obj_layout)
no_of_columns = obj_layout["qHyperCube"]["qSize"]["qcx"]
# print(no_of_columns)
width = no_of_columns
no_of_rows = obj_layout["qHyperCube"]["qSize"]["qcy"]
# print(no_of_rows)
height = no_of_rows
# height = 5

max_no_cells = no_of_columns * no_of_rows
nx_page = qixe.structs.nx_page(0, 0, no_of_columns, no_of_rows)
# hc_data = qixe.egoa.get_hypercube_stack_data(obj_handle, "/qHyperCubeDef", [nx_page], max_no_cells)
# print(hc_data)
hc_data = qixe.egoa.get_hypercube_stack_data(obj_handle, "/qHyperCubeDef", [nx_page], max_no_cells)['qDataPages'][0]['qData'][0]['qSubNodes']
print(hc_data)



# Transform the nested structure into a flat DataFrame
data_values = []
for node in hc_data:
    for sub_node in node['qSubNodes']:
        value = sub_node['qSubNodes'][0]['qValue'] if sub_node['qSubNodes'] else None
        data_values.append([node['qText'], sub_node['qText'], value])


# Extrahiere die qFallbackTitle-Werte für Dimensionen und Maße
dimension_titles = [dim['qFallbackTitle'] for dim in obj_layout["qHyperCube"]["qDimensionInfo"]]
measure_titles = [measure['qFallbackTitle'] for measure in obj_layout["qHyperCube"]["qMeasureInfo"]]
# Erstelle eine Liste von Spaltennamen (Kombination aus Dimensionen und Maßen)
column_names = dimension_titles + measure_titles

# Create DataFrame
df = pd.DataFrame(data_values, columns=column_names)

# Display the DataFrame
print(df)


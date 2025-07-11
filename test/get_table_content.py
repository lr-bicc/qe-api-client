from qe_api_client.engine import QixEngine
import math
import pandas as pd

url = 'ws://localhost:4848/app'
qixe = QixEngine(url=url)

# App ID holen
# doc_id = "f9e79d92-652b-4ba8-8487-84e2825b71c5"     # Sales KPI
doc_id = "Test.qvf"

# App öffnen
opened_doc = qixe.ega.open_doc(doc_id)
# print(opened_doc)

doc_handle = qixe.get_handle(opened_doc)

obj = qixe.eaa.get_object(doc_handle, "tshujdG")    # Bar chart: LapHp | Table: tshujdG | Pie chart: gYyUxS

obj_handle = qixe.get_handle(obj)

obj_layout = qixe.egoa.get_layout(obj_handle)
print(obj_layout["qInfo"]["qType"])
no_of_columns = obj_layout["qHyperCube"]["qSize"]["qcx"]
width = no_of_columns
no_of_rows = obj_layout["qHyperCube"]["qSize"]["qcy"]
height = int(math.floor(10000 / no_of_columns))
# height = 5


page = 0
hc_list = []

while no_of_rows > page * height:
    nx_page = qixe.structs.nx_page(0, page * height, width, height)
    hc_data = qixe.egoa.get_hypercube_data(handle=obj_handle, path="/qHyperCubeDef", pages=[nx_page])['qDataPages'][0]['qMatrix']
    hc_list.extend(hc_data)

    page += 1


# DataFrame nur mit dem Attribut "qText" erstellen
df = pd.DataFrame([[d['qText'] for d in sublist] for sublist in hc_list])


# Extrahiere die qFallbackTitle-Werte für Dimensionen und Maße
dimension_titles = [dim['qFallbackTitle'] for dim in obj_layout["qHyperCube"]["qDimensionInfo"]]
measure_titles = [measure['qFallbackTitle'] for measure in obj_layout["qHyperCube"]["qMeasureInfo"]]
# Erstelle eine Liste von Spaltennamen (Kombination aus Dimensionen und Maßen)
column_names = dimension_titles + measure_titles
# Zuweisen der Spaltennamen
df.columns = column_names

# DataFrame anzeigen
print(df)
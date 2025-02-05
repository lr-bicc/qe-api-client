from qe_api_client.engine import QixEngine

url = 'ws://localhost:4848/app'
qixe = QixEngine(url=url)

# App ID holen
# doc_id = "f9e79d92-652b-4ba8-8487-84e2825b71c5"     # Sales KPI
doc_id = "Test.qvf"

# App öffnen
opened_doc = qixe.ega.open_doc(doc_id)
# print(opened_doc)

doc_handle = qixe.get_handle(opened_doc)

df = qixe.get_chart_data(doc_handle, "tshujdG")   # Pivot: wPSYmr | Straight: tshujdG | Bar chart: LapHp | Pie chart: gYyUxS
print(df)
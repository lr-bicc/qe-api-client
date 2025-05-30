from qe_api_client.engine import QixEngine
import math
import pandas as pd

url = 'ws://localhost:4848/app'
qixe = QixEngine(url=url)

# url = "lr-analytics-test.lr-netz.local"
# user_directory = "LR"
# user_id = "!QlikSense"
# qlik_certs_path = "C:/LocalUserData/Certificates/Sense TEST"
# ca_certs = qlik_certs_path + "/root.pem"
# certfile = qlik_certs_path + "/client.pem"
# keyfile = qlik_certs_path + "/client_key.pem"
# qixe = QixEngine(url, user_directory, user_id, ca_certs, certfile, keyfile)

# App ID holen
# app_id = "0c6a91a3-4dc0-490e-ae0f-41391b39c2ec" # Bonus Competitions
# app_id = "f9e79d92-652b-4ba8-8487-84e2825b71c5"     # Sales KPI
# app_id = "3b9ef434-f4e9-4310-9cef-1347502bc39d"     # Stocks
# app_id = "0a64346c-da25-4fd5-b1a7-e3d897d270e3"     # Sales & Stocks
app_id = "Test.qvf"

# App öffnen
opened_app = qixe.ega.open_doc(app_id)

app_handle = qixe.get_handle(opened_app)

# qixe.select_in_field(app_handle=app_handle, field_name="TopicBox_ABC_Analysis", list_of_values=["ABC Analysis", "Detailed stock information", "Avg. sales per week + range of coverage", "Sales per month", "Sales per week"])

df = qixe.get_chart_data(app_handle=app_handle, obj_id="xPpxvy")
print(df.to_string())
df.to_csv('C:/Users/R.Vasilev/OneDrive - LR/Desktop/out.csv', index=False)

# Websocket-Verbindung schließen
QixEngine.disconnect(qixe)
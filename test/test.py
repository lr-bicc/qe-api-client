from qe_api_client.engine import QixEngine
import math
import pandas as pd

# url = 'ws://localhost:4848/app'
# qixe = QixEngine(url=url)

url = "lr-analytics-test.lr-netz.local"
user_directory = "LR"
user_id = "!QlikSense"
qlik_certs_path = "C:/LocalUserData/Certificates/Sense TEST"
ca_certs = qlik_certs_path + "/root.pem"
certfile = qlik_certs_path + "/client.pem"
keyfile = qlik_certs_path + "/client_key.pem"
qixe = QixEngine(url, user_directory, user_id, ca_certs, certfile, keyfile)

# App ID holen
doc_id = "0c6a91a3-4dc0-490e-ae0f-41391b39c2ec" # Bonus Competitions
# doc_id = "f9e79d92-652b-4ba8-8487-84e2825b71c5"     # Sales KPI
# doc_id = "Test.qvf"

# App öffnen
opened_doc = qixe.ega.open_doc(doc_id)
print(opened_doc)

doc_handle = qixe.get_handle(opened_doc)

# # Lineage-Daten aus der API holen
# lineage = qixe.eaa.get_lineage(doc_handle)
# print(lineage)
#
# # Erstelle den DataFrame und fülle fehlende Werte mit ""
# df = pd.DataFrame(lineage)  #.fillna("")
# df = df[(df["qDiscriminator"].notna()) | (df["qStatement"].notna())].fillna("")
# # df = df.reindex(columns=["qDiscriminator", "qStatement"]).fillna("")

df = qixe.get_app_lineage_info(doc_handle)

print(df)


# Websocket-Verbindung schließen
QixEngine.disconnect(qixe)
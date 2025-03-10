from qe_api_client.engine import QixEngine


# Connect to Qlik Sense Desktop engine
url = 'ws://localhost:4848/app'
qixe = QixEngine(url)

# Retrieves a list with all apps on the server containing meta data
apps_list = qixe.get_apps()
print(apps_list)

# close connection
QixEngine.disconnect(qixe)
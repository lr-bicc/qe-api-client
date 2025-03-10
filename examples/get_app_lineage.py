# Import engine package
from qe_api_client.engine import QixEngine


# Connect to Qlik Sense Desktop engine
url = 'ws://localhost:4848/app'
qixe = QixEngine(url)

# Create an app
app_name = "TestApp"
try:
    app_id = qixe.ega.create_app(app_name)['qAppId']
except KeyError:
    qixe.ega.delete_app(app_name)
    app_id = qixe.ega.create_app(app_name)['qAppId']

# Open app
opened_app = qixe.ega.open_doc(app_name)

# Get app handle
app_handle = qixe.get_handle(opened_app)

# Set script
with open('../test/test_data/ctrl00_script.qvs') as f:
    app_script = f.read()
script_result = qixe.eaa.set_script(app_handle, app_script)

# Reload app
reload_result = qixe.eaa.do_reload_ex(app_handle)

# Retrieves a list with an app lineage data
app_lineage = qixe.get_app_lineage(app_handle=app_handle)
print(app_lineage)

# close connection
QixEngine.disconnect(qixe)
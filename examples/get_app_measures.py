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

# Create measures
measure_1 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression1", mes_def="Sum(Expression1)",
                                       mes_label="'Expression 1'", mes_desc="Expression description 1",
                                       mes_tags=["exp1", "test"])
measure_2 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression2", mes_def="Sum(Expression2)",
                                       mes_label="'Expression 2'", mes_desc="Expression description 2",
                                       mes_tags=["exp2", "test"])
measure_3 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression3", mes_def="Sum(Expression3)",
                                       mes_label="'Expression 3'", mes_desc="Expression description 3",
                                       mes_tags=["exp3", "test"])

# Save app
save_result =qixe.eaa.do_save(app_handle, app_name)

# Retrieves a list with all dimensions in the app containing dimension metadata
measure_list = qixe.get_app_measures(app_handle=app_handle)
print(measure_list.to_string())

# close connection
QixEngine.disconnect(qixe)
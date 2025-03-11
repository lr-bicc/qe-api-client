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

# Create master dimensions
dim_1 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension1", dim_def="Dim1",
                                            dim_label="'Dimension 1'", dim_desc="Dimension description 1",
                                            dim_tags=["dim1", "test"])
dim_2 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension2", dim_def="Dim2",
                                            dim_label="'Dimension 2'", dim_desc="Dimension description 2",
                                            dim_tags=["dim2", "test"])
dim_3 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension3", dim_def="Dim3",
                                            dim_label="'Dimension 3'", dim_desc="Dimension description 3",
                                            dim_tags=["dim3", "test"])

# Save app
save_result =qixe.eaa.do_save(app_handle, app_name)

# Retrieves a list with all dimensions in the app containing dimension metadata
dimension_list = qixe.get_app_dimensions(app_handle=app_handle)
print(dimension_list.to_string())

# close connection
QixEngine.disconnect(qixe)
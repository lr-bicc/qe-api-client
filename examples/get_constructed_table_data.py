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

# Define dimensions and measures
list_of_dimensions = ["Dim1"]
list_of_measures = ["Sum(Expression1)"]

# Create dimensions and measures
dim_2 = qixe.create_single_master_dimension(app_handle, dim_title="Dimension2", dim_def="Dim2", dim_label="'Dimension 2'")
dim_2_id = dim_2["qGenericId"]
dim_3 = qixe.create_single_master_dimension(app_handle, dim_title="Dimension3", dim_def="Dim3", dim_label="'Dimension 3'")
dim_3_id = dim_3["qGenericId"]
exp_2 = qixe.create_master_measure(app_handle, "Expression2", "Sum(Expression2)", "Expression 2")
exp_2_id = exp_2["qGenericId"]
exp_3 = qixe.create_master_measure(app_handle, "Expression3", "Sum(Expression3)", "Expression 3")
exp_3_id = exp_3["qGenericId"]

# Create master dimensions and master measures
list_of_master_dimensions = [dim_2_id, dim_3_id]
list_of_master_measures = [exp_2_id, exp_3_id]

# Put the dimensions and the measures in a dataframe and print the results
df = qixe.get_constructed_table_data(app_handle, list_of_dimensions, list_of_measures, list_of_master_dimensions, list_of_master_measures)
print(df)

# delete app
qixe.ega.delete_app(app_id)

# close connection
QixEngine.disconnect(qixe)
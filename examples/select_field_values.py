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
list_of_dimensions = ["Dim1", "Dim2", "Dim3"]
list_of_measures = ["Sum(Expression1)"]


# Put the dimensions and the measures in a dataframe and print the results
df = qixe.get_constructed_table_data(app_handle=app_handle, list_of_dimensions=list_of_dimensions,
                                     list_of_measures=list_of_measures)
print("Data set before the selections:")
print("===============================")
print(df)
print("\n")

# Select values
selection_1 = qixe.select_in_field(app_handle=app_handle, field_name="Dim1", list_of_values=["A", "B"])
selection_2 = qixe.select_in_field(app_handle=app_handle, field_name="Dim3", list_of_values=["Z"])
print("Selections:")
print("===========")
print("Selection 1:", selection_1)
print("Selection 2:", selection_2)
print("\n")



# Put the dimensions and the measures in a dataframe and print the results
df = qixe.get_constructed_table_data(app_handle=app_handle, list_of_dimensions=list_of_dimensions,
                                     list_of_measures=list_of_measures)
print("Data set after the selections:")
print("==============================")
print(df)

# delete app
qixe.ega.delete_app(app_id)

# close connection
QixEngine.disconnect(qixe)
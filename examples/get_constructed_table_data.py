# Import utilities
import utilities as utils
# from test.create_master_measure import app_handle

# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Create a sample app
sample_app = utils.create_sample_app(conn)

# Get app handle
app_handle = sample_app["appHandle"]

# Get IDs of master dimensions and measures
dim_2_id = sample_app["dimension2Id"]
dim_3_id = sample_app["dimension3Id"]
measure_2_id = sample_app["measure2Id"]
measure_3_id = sample_app["measure3Id"]

# Self-defined dimensions and measures
list_of_dimensions = ["Dim1"]
list_of_measures = ["Sum(Expression1)"]

# Create master dimensions and master measures
list_of_master_dimensions = [dim_2_id, dim_3_id]
list_of_master_measures = [measure_2_id, measure_3_id]

# Put the dimensions and the measures in a dataframe and print the results
df = conn.get_constructed_table_data(app_handle, list_of_dimensions, list_of_measures, list_of_master_dimensions, list_of_master_measures)
print(df.to_string())

# delete app
utils.delete_sample_app(conn)

# close engine connection
utils.close_connection(conn)
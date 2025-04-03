# Import utilities
import utilities as utils


# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Create a sample app
app_handle = utils.create_sample_app(conn)

# Define dimensions and measures
list_of_dimensions = ["Dim1"]
list_of_measures = ["Sum(Expression1)"]

# Create dimensions and measures
dim_2 = conn.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension2", dim_def="Dim2", dim_label="'Dimension 2'")
dim_2_id = dim_2["qGenericId"]
dim_3 = conn.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension3", dim_def="Dim3", dim_label="'Dimension 3'")
dim_3_id = dim_3["qGenericId"]
exp_2 = conn.create_master_measure(app_handle=app_handle, mes_title="Expression2", mes_def="Sum(Expression2)", mes_label="'Expression 2'")
exp_2_id = exp_2["qGenericId"]
exp_3 = conn.create_master_measure(app_handle=app_handle, mes_title="Expression3", mes_def="Sum(Expression3)", mes_label="'Expression 3'")
exp_3_id = exp_3["qGenericId"]

# Create master dimensions and master measures
list_of_master_dimensions = [dim_2_id, dim_3_id]
list_of_master_measures = [exp_2_id, exp_3_id]

# Put the dimensions and the measures in a dataframe and print the results
df = conn.get_constructed_table_data(app_handle, list_of_dimensions, list_of_measures, list_of_master_dimensions, list_of_master_measures)
print(df.to_string())

# delete app
utils.delete_sample_app(conn)

# close engine connection
utils.close_connection(conn)
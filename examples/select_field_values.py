# Import utilities
import utilities as utils


# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Create a sample app
sample_app = utils.create_sample_app(conn)

# Get app handle
app_handle = sample_app["appHandle"]

# Define dimensions and measures
list_of_dimensions = ["Dim1", "Dim2", "Dim3"]
list_of_measures = ["Sum(Expression1)"]


# Put the dimensions and the measures in a dataframe and print the results
df = conn.get_constructed_table_data(app_handle=app_handle, list_of_dimensions=list_of_dimensions,
                                     list_of_measures=list_of_measures)
print("Data set before the selections:")
print("===============================")
print(df)
print("\n")

# Select values
selection_1 = conn.select_in_field(app_handle=app_handle, field_name="Dim1", list_of_values=["A", "B"])
selection_2 = conn.select_in_field(app_handle=app_handle, field_name="Dim3", list_of_values=["Z"])
print("Selections:")
print("===========")
print("Selection 1:", selection_1)
print("Selection 2:", selection_2)
print("\n")


# Put the dimensions and the measures in a dataframe and print the results
df = conn.get_constructed_table_data(app_handle=app_handle, list_of_dimensions=list_of_dimensions,
                                     list_of_measures=list_of_measures)
print("Data set after the selections:")
print("==============================")
print(df)

# Save app
utils.save_sample_app(conn, app_handle)

# close engine connection
utils.close_connection(conn)
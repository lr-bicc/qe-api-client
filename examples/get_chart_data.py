# Import utilities
import utilities as utils


# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Create a sample app
sample_app = utils.create_sample_app(conn)

# Get app handle
app_handle = sample_app[0]

# Get table id
table_1_id = sample_app[9]

# Get pivot table id
pivot_table_1_id = sample_app[12]

# Get straight table id
sn_table_1_id = sample_app[15]

# Get new pivot table id
sn_pivot_table_1_id = sample_app[18]

# Retrieves the content of the table as dataframe
table_data = conn.get_chart_data(app_handle, table_1_id)
print("Table content:")
print("=================================")
print(table_data.to_string())
print("\n")

# Retrieves the content of the pivot table as dataframe
pivot_table_data = conn.get_chart_data(app_handle, pivot_table_1_id)
print("Pivot table content:")
print("=================================")
print(pivot_table_data.to_string())
print("\n")

# Retrieves the content of the straight table as dataframe
sn_table_data = conn.get_chart_data(app_handle, sn_table_1_id)
print("Straight table content:")
print("=================================")
print(sn_table_data.to_string())
print("\n")

# Retrieves the content of the new pivot table as dataframe
sn_pivot_table_data = conn.get_chart_data(app_handle, sn_pivot_table_1_id)
print("New pivot table content:")
print("=================================")
print(sn_pivot_table_data.to_string())
print("\n")

# close engine connection
utils.close_connection(conn)
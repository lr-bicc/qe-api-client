# Import utilities
import utilities as utils


# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Create a sample app
app_handle = utils.create_sample_app(conn)

# Create sample master dimensions
utils.create_sample_master_dimensions(conn, app_handle)

# Retrieves a list with all dimensions in the app containing dimension metadata
dimension_list = conn.get_app_dimensions(app_handle)
print(dimension_list.to_string())

# close engine connection
utils.close_connection(conn)
# Import utilities
import utilities as utils


# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Create a sample app
app_handle = utils.create_sample_app(conn)

# Retrieves a list with all fields in the app containing field metadata
fields_list = conn.get_app_fields(app_handle=app_handle)
print(fields_list)

# close engine connection
utils.close_connection(conn)
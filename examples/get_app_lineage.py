# Import utilities
import utilities as utils


# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Create a sample app
sample_app = utils.create_sample_app(conn)

# Get app handle
app_handle = sample_app["appHandle"]

# Retrieves a list with an app lineage data
app_lineage = conn.get_app_lineage(app_handle)
print(app_lineage)

# close engine connection
utils.close_connection(conn)
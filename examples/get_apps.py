# Import utilities
import utilities as utils


# Connect to Qlik Sense Desktop engine
conn = utils.create_connection()

# Retrieves a list with all apps on the server containing meta data
apps_list = conn.get_apps()
print(apps_list)

# close engine connection
utils.close_connection(conn)
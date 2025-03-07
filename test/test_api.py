from qe_api_client.engine import QixEngine
from qe_api_client.structs import field_value

# url = 'lr-analytics-test.lr-netz.local'
# user_directory = 'LR'
# user_id = 'r.vasilev'
# ca_certs = 'C:\\LocalUserData\\Certificates\\Sense TEST\\root.pem'
# certfile = 'C:\\LocalUserData\\Certificates\\Sense TEST\\client.pem'
# keyfile = 'C:\\LocalUserData\\Certificates\\Sense TEST\\client_key.pem'
# qixe = QixEngine(url=url, user_directory=user_directory, user_id=user_id, ca_certs=ca_certs, certfile=certfile,
#                  keyfile=keyfile)

url = 'ws://localhost:4848/app'
qixe = QixEngine(url)
opened_app = qixe.ega.open_doc("Test")
# print(opened_app)
app_handle = qixe.get_handle(opened_app)
# print(app_handle)

list_of_values = ["A", "C"]

test = qixe.select_in_field(app_handle, "Dim1", ["A", "B"])
print(test)

# field = qixe.eaa.get_field(app_handle, "Dim1")
# print(field)
#
# fld_handle = qixe.get_handle(field)
# print(fld_handle)

# selected_value = qixe.efa.select(field_handle, "B")
# print(selected_value)

# fld_value_1 = qixe.structs.field_value("A")
# fld_value_2 = qixe.structs.field_value("C")
# selected_values = qixe.efa.select_values(fld_handle, [fld_value_1, fld_value_2])

# values_to_select = []
# for val in list_of_values:
#     fld_value = qixe.structs.field_value(val)
#     values_to_select.append(fld_value)
# response = qixe.efa.select_values(fld_handle, values_to_select)
# print(response)

df = qixe.get_constructed_table_data(app_handle, [], [],
                                     ["BjKvssq", "48a5672b-e9b3-4f96-8ff4-480f606e3c14"],
                                     ["snmpR", "1ad7060c-56ec-46d1-b83a-ff1393e0b236"])

print(df)

# Websocket-Verbindung schließen
QixEngine.disconnect(qixe)

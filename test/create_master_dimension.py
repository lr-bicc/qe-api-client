from qe_api_client.engine import QixEngine

url = 'ws://localhost:4848/app'
qixe = QixEngine(url)
opened_app = qixe.ega.open_doc("Test")
# print(opened_app)
app_handle = qixe.get_handle(opened_app)
# print(app_handle)


# nx_info = qixe.structs.nx_info("dimension")
# lb_dim_def_1 = qixe.structs.nx_library_dimension_def(["Dim1"], [""], "'Dimension 1'")
# gen_dim_props_1 = qixe.structs.generic_dimension_properties(nx_info, lb_dim_def_1, "Dim 1")
# master_dim_1 = qixe.eaa.create_dimension(app_handle, gen_dim_props_1)
# print(master_dim_1)

dim_1 = qixe.create_single_master_dimension(app_handle, dim_title="Dim 1", dim_def="Dim1", dim_label="'Dimension 1'")
dim_1_id = dim_1["qGenericId"]
print(dim_1)

dim_des = qixe.eaa.destroy_dimension(app_handle, dim_1_id)
print(dim_des)


# Websocket-Verbindung schließen
QixEngine.disconnect(qixe)

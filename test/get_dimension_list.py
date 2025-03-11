from qe_api_client.engine import QixEngine

url = 'ws://localhost:4848/app'
qixe = QixEngine(url)
opened_app = qixe.ega.open_doc("Test")
# print(opened_app)
app_handle = qixe.get_handle(opened_app)
# print(app_handle)


nx_info = qixe.structs.nx_info("dimension")
print(nx_info)

dimension_list_def_ = qixe.structs.dimension_list_def()

generic_object_properties = qixe.structs.generic_object_properties(info=nx_info, prop_name="qDimensionListDef", prop_def=dimension_list_def_)
print("Generic Object Properties:", generic_object_properties)

dimension_list = qixe.eaa.create_session_object(app_handle, generic_object_properties)
print(dimension_list)

dimension_list_handle = qixe.get_handle(dimension_list)
print(dimension_list_handle)

dimension_list_layout = qixe.egoa.get_layout(dimension_list_handle)
print(dimension_list_layout)
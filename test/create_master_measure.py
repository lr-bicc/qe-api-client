from qe_api_client.engine import QixEngine

url = 'ws://localhost:4848/app'
qixe = QixEngine(url)
opened_app = qixe.ega.open_doc("Test")
# print(opened_app)
app_handle = qixe.get_handle(opened_app)
# print(app_handle)


# nx_info = qixe.structs.nx_info("measure")
# lb_mes_def_1 = qixe.structs.nx_inline_measure_def("Sum(Expression3)", "Expression3")
# print(lb_mes_def_1)
# gen_mes_props_1 = qixe.structs.generic_measure_properties(nx_info, lb_mes_def_1, "Expression 3")
# print(gen_mes_props_1)
# master_mes_1 = qixe.eaa.create_measure(app_handle, gen_mes_props_1)
# print(master_mes_1)

mes_1 = qixe.create_master_measure(app_handle, "Expression3", "Sum(Expression3)", "'Expression 3'")
mes_1_id = mes_1["qGenericId"]
print(mes_1)
mes_1_handle = qixe.get_handle(mes_1)

mes_1_layout = qixe.egoa.get_layout(mes_1_handle)
print(mes_1_layout)

#
# dim_des = qixe.eaa.destroy_dimension(app_handle, dim_1_id)
# print(dim_des)


# Websocket-Verbindung schließen
QixEngine.disconnect(qixe)

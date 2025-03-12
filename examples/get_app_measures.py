# Import engine package
from qe_api_client.engine import QixEngine
import pandas as pd


# Connect to Qlik Sense Desktop engine
url = 'ws://localhost:4848/app'
qixe = QixEngine(url)

# Create an app
app_name = "TestApp"
try:
    app_id = qixe.ega.create_app(app_name)['qAppId']
except KeyError:
    qixe.ega.delete_app(app_name)
    app_id = qixe.ega.create_app(app_name)['qAppId']

# Open app
opened_app = qixe.ega.open_doc(app_name)

# Get app handle
app_handle = qixe.get_handle(opened_app)

# Set script
with open('../test/test_data/ctrl00_script.qvs') as f:
    app_script = f.read()
script_result = qixe.eaa.set_script(app_handle, app_script)

# Reload app
reload_result = qixe.eaa.do_reload_ex(app_handle)

# Create measures
measure_1 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression1", mes_def="Sum(Expression1)",
                                       mes_label="'Expression 1'", mes_desc="Expression description 1",
                                       mes_tags=["exp1", "test"])
measure_2 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression2", mes_def="Sum(Expression2)",
                                       mes_label="'Expression 2'", mes_desc="Expression description 2",
                                       mes_tags=["exp2", "test"])
measure_3 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression3", mes_def="Sum(Expression3)",
                                       mes_label="'Expression 3'", mes_desc="Expression description 3",
                                       mes_tags=["exp3", "test"])

# Save app
save_result =qixe.eaa.do_save(app_handle, app_name)

# Retrieves a list with all dimensions in the app containing dimension metadata
measure_list = qixe.get_app_measures(app_handle=app_handle)
print(measure_list.to_string())


# # Open app
# opened_app = qixe.ega.open_doc("Test")
#
# # Get app handle
# app_handle = qixe.get_handle(opened_app)



# # Define the parameters of the session object
# nx_info = qixe.structs.nx_info(obj_type="MeasureList")
# measure_list_def = qixe.structs.measure_list_def()
# gen_obj_props = qixe.structs.generic_object_properties(info=nx_info, prop_name="qMeasureListDef",
#                                                        prop_def=measure_list_def)
#
# # Create session object
# session = qixe.eaa.create_session_object(app_handle, gen_obj_props)
#
# # Get session handle
# session_handle = qixe.get_handle(session)
#
# # Get session object data
# session_layout = qixe.egoa.get_layout(session_handle)
#
# # Get the measure list as Dictionary structure
# measure_list = session_layout["qMeasureList"]["qItems"]
#
# # Define the DataFrame structure
# df_measure_list = pd.DataFrame(columns=["qInfo", "qMeasure", "qMeta"])
#
# for measure in measure_list:
#     # Get measure ID
#     measure_id = measure["qInfo"]["qId"]
#     # Get measure
#     measure_result = qixe.egma.get_measure(app_handle=app_handle, measure_id=measure_id)
#     # Get measure handle
#     measure_handle = qixe.get_handle(measure_result)
#     # Get session object data
#     measure_layout = qixe.egoa.get_layout(measure_handle)
#
#     # Concatenate the measure metadata to the DataFrame structure
#     df_measure_list.loc[len(df_measure_list)] = measure_layout
#
#
# # Resolve the dictionary structure of attribute "qInfo"
# df_measure_list_expanded = (df_measure_list["qInfo"].apply(pd.Series).add_prefix("qInfo_"))
# df_measure_list = df_measure_list.drop(columns=["qInfo"]).join(df_measure_list_expanded)
#
# # Resolve the dictionary structure of attribute "qMeasure"
# df_measure_list_expanded = (df_measure_list["qMeasure"].apply(pd.Series).add_prefix("qMeasure_"))
# df_measure_list = df_measure_list.drop(columns=["qMeasure"]).join(df_measure_list_expanded)
#
# # Resolve the dictionary structure of attribute "qMeta"
# df_measure_list_expanded = (df_measure_list["qMeta"].apply(pd.Series).add_prefix("qMeta_"))
# df_measure_list = df_measure_list.drop(columns=["qMeta"]).join(df_measure_list_expanded)
#
# # Resolve the dictionary structure of attribute "qMeasure_qNumFormat"
# df_measure_list_expanded = (df_measure_list["qMeasure_qNumFormat"].apply(pd.Series).add_prefix("qMeasure_qNumFormat_"))
# df_measure_list = df_measure_list.drop(columns=["qMeasure_qNumFormat"]).join(df_measure_list_expanded)
#
# # Resolve the dictionary structure of attribute "qMeasure_coloring"
# try:
#     df_measure_list_expanded = (df_measure_list["qMeasure_coloring"].apply(pd.Series).add_prefix("qMeasure_coloring_"))
#     df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring"]).join(df_measure_list_expanded)
# except KeyError:
#     df_measure_list["qMeasure_coloring"] = ""
#
# # Resolve the dictionary structure of attribute "qMeasure_coloring_baseColor"
# try:
#     df_measure_list_expanded = (df_measure_list["qMeasure_coloring_baseColor"].apply(pd.Series).add_prefix("qMeasure_coloring_baseColor_"))
#     df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring_baseColor"]).join(df_measure_list_expanded)
# except KeyError:
#     df_measure_list["qMeasure_coloring_baseColor"] = ""

# # Resolve the dictionary structure of attribute "qMeasure_coloring_baseColor_gradient"
# try:
#     df_measure_list_expanded = (df_measure_list["qMeasure_coloring_baseColor_gradient"].apply(pd.Series).add_prefix("qMeasure_coloring_baseColor_gradient_"))
#     df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring_baseColor_gradient"]).join(df_measure_list_expanded)
# except KeyError:
#     df_measure_list["qMeasure_coloring_baseColor_gradient"] = ""

# # Resolve the dictionary structure of attribute "qMeasure_coloring_baseColor_gradient_0"
# try:
#     df_measure_list_expanded = (df_measure_list["qMeasure_coloring_baseColor_gradient_0"].apply(pd.Series).add_prefix("qMeasure_coloring_baseColor_gradient_0_"))
#     df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring_baseColor_gradient_0"]).join(df_measure_list_expanded)
# except KeyError:
#     df_measure_list["qMeasure_coloring_baseColor_gradient_0"] = ""
#
# # Resolve the dictionary structure of attribute "qMeasure_coloring_baseColor_gradient_0_qMeasure_coloring_baseColor_gradient_0"
# try:
#     df_measure_list_expanded = (df_measure_list["qMeasure_coloring_baseColor_gradient_0_qMeasure_coloring_baseColor_gradient_0"].apply(pd.Series).add_prefix("qMeasure_coloring_baseColor_gradient_0_qMeasure_coloring_baseColor_gradient_0_"))
#     df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring_baseColor_gradient_0_qMeasure_coloring_baseColor_gradient_0"]).join(df_measure_list_expanded)
# except KeyError:
#     df_measure_list["qMeasure_coloring_baseColor_gradient_0_qMeasure_coloring_baseColor_gradient_0"] = ""

# # Resolve the list structure of attribute
# df_dimension_list = df_dimension_list.explode(['qDimInfos', 'qDim_qFieldDefs', 'qDim_qFieldLabels'])
#
# # Resolve the dictionary structure of attribute "qDimInfos"
# df_dimension_list_expanded = (df_dimension_list["qDimInfos"].apply(pd.Series).add_prefix("qDimInfos_"))
# index = df_dimension_list_expanded.index
# df_dimension_list_expanded = df_dimension_list_expanded[~index.duplicated(keep="first")]
# df_dimension_list = df_dimension_list.drop(columns=["qDimInfos"]).join(df_dimension_list_expanded)

# print(df_measure_list.to_string())


# close connection
QixEngine.disconnect(qixe)
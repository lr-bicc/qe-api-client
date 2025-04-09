def create_connection():
    # Import engine package
    from qe_api_client.engine import QixEngine

    # Connect to Qlik Sense Desktop engine
    url = 'ws://localhost:4848/app'
    qixe = QixEngine(url)

    return qixe


def create_sample_app(qixe):
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
    qixe.eaa.set_script(app_handle, app_script)

    # Reload app
    qixe.eaa.do_reload_ex(app_handle)

    # Create sample master dimensions
    dim_1 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension1", dim_def="Dim1",
                                        dim_label="'Dimension 1'", dim_desc="Dimension description 1",
                                        dim_tags=["dim1", "test"])
    dim_2 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension2", dim_def="Dim2",
                                        dim_label="'Dimension 2'", dim_desc="Dimension description 2",
                                        dim_tags=["dim2", "test"])
    dim_3 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension3", dim_def="Dim3",
                                        dim_label="'Dimension 3'", dim_desc="Dimension description 3",
                                        dim_tags=["dim3", "test"])

    # Create sample master measures
    qixe.create_master_measure(app_handle=app_handle, mes_title="Expression1", mes_def="Sum(Expression1)",
                               mes_label="'Expression 1'", mes_desc="Expression description 1",
                               mes_tags=["exp1", "test"])
    qixe.create_master_measure(app_handle=app_handle, mes_title="Expression2", mes_def="Sum(Expression2)",
                               mes_label="'Expression 2'", mes_desc="Expression description 2",
                               mes_tags=["exp2", "test"])
    qixe.create_master_measure(app_handle=app_handle, mes_title="Expression3", mes_def="Sum(Expression3)",
                               mes_label="'Expression 3'", mes_desc="Expression description 3",
                               mes_tags=["exp3", "test"])

    # Create sheets
    no_of_rows_sheet_1 = 12
    no_of_cols_sheet_1 = no_of_rows_sheet_1 * 2
    no_of_rows_sheet_2 = 42
    no_of_cols_sheet_2 = no_of_rows_sheet_2 * 2
    no_of_rows_sheet_3 = 42
    no_of_cols_sheet_3 = no_of_rows_sheet_3 * 2

    sheet_1 = qixe.create_sheet(app_handle=app_handle, sheet_title="My New Sheet 1", sheet_desc="Sheet description",
                                no_of_rows=no_of_rows_sheet_1)
    sheet_1_handle = qixe.get_handle(sheet_1)
    sheet_2 = qixe.create_sheet(app_handle=app_handle, sheet_title="My New Sheet 2", sheet_desc="Sheet description",
                                no_of_rows=no_of_rows_sheet_2)
    sheet_2_handle = qixe.get_handle(sheet_2)
    sheet_3 = qixe.create_sheet(app_handle=app_handle, sheet_title="My New Sheet 3", sheet_desc="Sheet description",
                                no_of_rows=no_of_rows_sheet_3)
    sheet_3_handle = qixe.get_handle(sheet_3)

    # Create filterpane
    filterpane = qixe.create_filterpane_frame(handle=sheet_1_handle, no_of_rows_sheet=no_of_rows_sheet_1, col=0, row=0,
                                              colspan=no_of_cols_sheet_1, rowspan=1)
    filterpane_handle = qixe.get_handle(filterpane)

    dim_1_id = qixe.get_id(dim_1)
    field_title_1 = "Dimension 1"
    list_object_1 = qixe.create_list_object(handle=filterpane_handle, dim_id=dim_1_id, field_title=field_title_1)

    dim_2_id = qixe.get_id(dim_2)
    field_title_2 = "Dimension 2"
    list_object_2 = qixe.create_list_object(handle=filterpane_handle, dim_id=dim_2_id, field_title=field_title_2)

    dim_3_id = qixe.get_id(dim_3)
    field_title_3 = "Dimension 3"
    list_object_3 = qixe.create_list_object(handle=filterpane_handle, dim_id=dim_3_id, field_title=field_title_3)

    field_def = "Alpha"
    field_title_4 = "Alpha"
    list_object_4 = qixe.create_list_object(handle=filterpane_handle, field_def=field_def, field_title=field_title_4)

    # Save app
    save_sample_app(qixe, app_handle)

    return app_handle


def save_sample_app(qixe, app_handle: int):
    qixe.eaa.do_save(app_handle, "TestApp")


def close_connection(qixe):
    # Import engine package
    from qe_api_client.engine import QixEngine

    QixEngine.disconnect(qixe)


def delete_sample_app(qixe):
    qixe.ega.delete_app("TestApp")
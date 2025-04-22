from qe_api_client.structs import hypercube_def


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
    with open('sample_app_script.qvs') as f:
        app_script = f.read()
    qixe.eaa.set_script(app_handle, app_script)

    # Reload app
    qixe.eaa.do_reload_ex(app_handle)

    # Save app
    save_sample_app(qixe, app_handle)


    ####################################################################################################################
    # Create sample master dimensions
    ####################################################################################################################

    dim_1 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension1", dim_def="Dim1",
                                        dim_label="'Dimension 1'", dim_desc="Dimension description 1",
                                        dim_tags=["dim1", "test"])
    dim_1_id = qixe.get_id(dim_1)

    dim_2 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension2", dim_def="Dim2",
                                        dim_label="'Dimension 2'", dim_desc="Dimension description 2",
                                        dim_tags=["dim2", "test"])
    dim_2_id = qixe.get_id(dim_2)

    dim_3 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension3", dim_def="Dim3",
                                        dim_label="'Dimension 3'", dim_desc="Dimension description 3",
                                        dim_tags=["dim3", "test"])
    dim_3_id = qixe.get_id(dim_3)


    ####################################################################################################################
    # Create sample master measures
    ####################################################################################################################

    measure_1 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression1", mes_def="Sum(Expression1)",
                               mes_label="'Expression 1'", mes_desc="Expression description 1",
                               mes_tags=["exp1", "test"])
    measure_1_id = qixe.get_id(measure_1)

    measure_2 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression2", mes_def="Sum(Expression2)",
                               mes_label="'Expression 2'", mes_desc="Expression description 2",
                               mes_tags=["exp2", "test"])
    measure_2_id = qixe.get_id(measure_2)

    measure_3 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression3", mes_def="Sum(Expression3)",
                               mes_label="'Expression 3'", mes_desc="Expression description 3",
                               mes_tags=["exp3", "test"])
    measure_3_id = qixe.get_id(measure_3)


    ####################################################################################################################
    # Create sheets
    ####################################################################################################################

    no_of_rows_sheet_1 = 12
    no_of_cols_sheet_1 = no_of_rows_sheet_1 * 2
    no_of_rows_sheet_2 = 42
    no_of_cols_sheet_2 = no_of_rows_sheet_2 * 2
    no_of_rows_sheet_3 = 42
    no_of_cols_sheet_3 = no_of_rows_sheet_3 * 2

    sheet_1 = qixe.create_sheet(app_handle=app_handle, sheet_title="My New Sheet 1", sheet_desc="Sheet description",
                                no_of_rows=no_of_rows_sheet_1)
    sheet_1_handle = qixe.get_handle(sheet_1)
    sheet_1_id = qixe.get_id(sheet_1)
    sheet_2 = qixe.create_sheet(app_handle=app_handle, sheet_title="My New Sheet 2", sheet_desc="Sheet description",
                                no_of_rows=no_of_rows_sheet_2)
    sheet_2_handle = qixe.get_handle(sheet_2)
    sheet_2_id = qixe.get_id(sheet_2)
    sheet_3 = qixe.create_sheet(app_handle=app_handle, sheet_title="My New Sheet 3", sheet_desc="Sheet description",
                                no_of_rows=no_of_rows_sheet_3)
    sheet_3_handle = qixe.get_handle(sheet_3)
    sheet_3_id = qixe.get_id(sheet_3)



    ####################################################################################################################
    # Create objects on sheet 1
    ####################################################################################################################

    # ------------------------------------------------------------------------------------------------------------------
    # Create filterpane
    # ------------------------------------------------------------------------------------------------------------------

    # Create filterpane frame
    filterpane_1 = qixe.create_filterpane_frame(handle=sheet_1_handle, no_of_rows_sheet=no_of_rows_sheet_1, col=0, row=0,
                                              colspan=no_of_cols_sheet_1, rowspan=1)
    filterpane_1_id = qixe.get_id(filterpane_1)

    # Create list objects
    filterpane_1_handle = qixe.get_handle(filterpane_1)
    qixe.create_list_object(handle=filterpane_1_handle, dim_id=dim_1_id, field_title="Dimension 1")
    qixe.create_list_object(handle=filterpane_1_handle, dim_id=dim_2_id, field_title="Dimension 2")
    qixe.create_list_object(handle=filterpane_1_handle, dim_id=dim_3_id, field_title="Dimension 3")
    qixe.create_list_object(handle=filterpane_1_handle, field_def="Alpha", field_title="Alpha")


    # ------------------------------------------------------------------------------------------------------------------
    # Create table
    # ------------------------------------------------------------------------------------------------------------------

    # Create the structure of tne dimensions
    table_nx_inline_dimension_def_1 = qixe.structs.nx_inline_dimension_def()
    table_nx_inline_dimension_def_2 = qixe.structs.nx_inline_dimension_def()
    table_nx_inline_dimension_def_3 = qixe.structs.nx_inline_dimension_def()
    table_hc_dim_1 = qixe.structs.nx_dimension(library_id=dim_1_id, dim_def=table_nx_inline_dimension_def_1)
    table_hc_dim_2 = qixe.structs.nx_dimension(library_id=dim_2_id, dim_def=table_nx_inline_dimension_def_2)
    table_hc_dim_3 = qixe.structs.nx_dimension(library_id=dim_3_id, dim_def=table_nx_inline_dimension_def_3)
    table_hc_dim_list = [table_hc_dim_1, table_hc_dim_2, table_hc_dim_3]

    # Create the structure of tne measures
    table_nx_inline_measure_def_1 = qixe.structs.nx_inline_measure_def()
    table_nx_inline_measure_def_2 = qixe.structs.nx_inline_measure_def()
    table_nx_inline_measure_def_3 = qixe.structs.nx_inline_measure_def()
    table_hc_mes_1 = qixe.structs.nx_measure(library_id=measure_1_id, mes_def=table_nx_inline_measure_def_1)
    table_hc_mes_2 = qixe.structs.nx_measure(library_id=measure_2_id, mes_def=table_nx_inline_measure_def_2)
    table_hc_mes_3 = qixe.structs.nx_measure(library_id=measure_3_id, mes_def=table_nx_inline_measure_def_3)
    table_hc_mes_list = [table_hc_mes_1, table_hc_mes_2, table_hc_mes_3]

    # Create hypercube structure for table
    hypercube_def_table = qixe.structs.hypercube_def(dimensions=table_hc_dim_list, measures=table_hc_mes_list,
                                                     column_order=[0, 1, 2, 3, 4, 5],
                                                     column_widths=[-1, -1, -1, -1, -1, -1])

    # Create table
    table_1 = qixe.create_chart(handle=sheet_1_handle, obj_type="table", hypercube_def=hypercube_def_table,
                              no_of_rows_sheet=no_of_rows_sheet_1, col=0, row=1, colspan=no_of_cols_sheet_1,
                              rowspan=no_of_rows_sheet_1-1)
    table_1_id = qixe.get_id(table_1)



    ####################################################################################################################
    # Create objects on sheet 2
    ####################################################################################################################

    # ------------------------------------------------------------------------------------------------------------------
    # Create filterpane
    # ------------------------------------------------------------------------------------------------------------------

    # Create filterpane frame
    filterpane_2 = qixe.create_filterpane_frame(handle=sheet_2_handle, no_of_rows_sheet=no_of_rows_sheet_2, col=0, row=0,
                                              colspan=no_of_cols_sheet_2, rowspan=3)
    filterpane_2_id = qixe.get_id(filterpane_2)

    # Create list objects
    filterpane_2_handle = qixe.get_handle(filterpane_2)
    qixe.create_list_object(handle=filterpane_2_handle, dim_id=dim_1_id, field_title="Dimension 1")
    qixe.create_list_object(handle=filterpane_2_handle, dim_id=dim_2_id, field_title="Dimension 2")
    qixe.create_list_object(handle=filterpane_2_handle, dim_id=dim_3_id, field_title="Dimension 3")
    qixe.create_list_object(handle=filterpane_2_handle, field_def="Alpha", field_title="Alpha")


    # ------------------------------------------------------------------------------------------------------------------
    # Create pivot table
    # ------------------------------------------------------------------------------------------------------------------

    # Create the structure of tne dimensions
    pivot_table_nx_inline_dimension_def_1 = qixe.structs.nx_inline_dimension_def()
    pivot_table_nx_inline_dimension_def_2 = qixe.structs.nx_inline_dimension_def()
    pivot_table_nx_inline_dimension_def_3 = qixe.structs.nx_inline_dimension_def()
    pivot_table_hc_dim_1 = qixe.structs.nx_dimension(library_id=dim_1_id, dim_def=pivot_table_nx_inline_dimension_def_1)
    pivot_table_hc_dim_2 = qixe.structs.nx_dimension(library_id=dim_2_id, dim_def=pivot_table_nx_inline_dimension_def_2)
    pivot_table_hc_dim_3 = qixe.structs.nx_dimension(library_id=dim_3_id, dim_def=pivot_table_nx_inline_dimension_def_3)
    pivot_table_hc_dim_list = [pivot_table_hc_dim_1, pivot_table_hc_dim_2, pivot_table_hc_dim_3]

    # Create the structure of tne measures
    pivot_table_nx_inline_measure_def_1 = qixe.structs.nx_inline_measure_def()
    pivot_table_nx_inline_measure_def_2 = qixe.structs.nx_inline_measure_def()
    pivot_table_nx_inline_measure_def_3 = qixe.structs.nx_inline_measure_def()
    pivot_table_hc_mes_1 = qixe.structs.nx_measure(library_id=measure_1_id, mes_def=pivot_table_nx_inline_measure_def_1)
    pivot_table_hc_mes_2 = qixe.structs.nx_measure(library_id=measure_2_id, mes_def=pivot_table_nx_inline_measure_def_2)
    pivot_table_hc_mes_3 = qixe.structs.nx_measure(library_id=measure_3_id, mes_def=pivot_table_nx_inline_measure_def_3)
    pivot_table_hc_mes_list = [pivot_table_hc_mes_1, pivot_table_hc_mes_2, pivot_table_hc_mes_3]

    # Create hypercube structure for pivot table
    hypercube_def_pivot_table = qixe.structs.hypercube_def(dimensions=pivot_table_hc_dim_list, measures=pivot_table_hc_mes_list,
                                                           inter_column_sort_order=[0, 1, 2, -1], mode="P")

    # Create pivot table
    pivot_table_1 = qixe.create_chart(handle=sheet_2_handle, obj_type="pivot-table", hypercube_def=hypercube_def_pivot_table,
                              no_of_rows_sheet=no_of_rows_sheet_2, col=0, row=3, colspan=no_of_cols_sheet_2,
                              rowspan=no_of_rows_sheet_2 - 3)
    pivot_table_1_id = qixe.get_id(pivot_table_1)

    # Save app
    save_sample_app(qixe, app_handle)

    return (app_handle, dim_1_id, dim_2_id, dim_3_id, measure_1_id, measure_2_id, measure_3_id, sheet_1_id,
            filterpane_1_id, table_1_id, sheet_2_id, filterpane_2_id, pivot_table_1_id, sheet_3_id)


def save_sample_app(qixe, app_handle: int):
    qixe.eaa.do_save(app_handle, "TestApp")


def close_connection(qixe):
    # Import engine package
    from qe_api_client.engine import QixEngine

    QixEngine.disconnect(qixe)


def delete_sample_app(qixe):
    qixe.ega.delete_app("TestApp")
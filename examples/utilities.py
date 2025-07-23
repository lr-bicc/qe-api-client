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

    dim_1_value_color_1 = qixe.structs.value_color(value="A", color="#117734")
    dim_1_value_color_2 = qixe.structs.value_color(value="B", color="#e32f50")
    dim_1_value_color_3 = qixe.structs.value_color(value="C", color="#009cda")
    dim_1_value_colors = [dim_1_value_color_1, dim_1_value_color_2, dim_1_value_color_3]
    dim_1 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension1", dim_def="Dim1",
                                                dim_label="'Dimension 1'", dim_desc="Dimension description 1",
                                                dim_tags=["dim1", "test"], dim_color="#006580", null_value_color="#b2b5b7",
                                                other_value_color="#ddcc77", value_colors=dim_1_value_colors)
    dim_1_id = qixe.get_id(dim_1)

    dim_2 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension2", dim_def="Dim2",
                                        dim_label="'Dimension 2'", dim_desc="Dimension description 2",
                                        dim_tags=["dim2", "test"], dim_color="#87205d", palette="100")
    dim_2_id = qixe.get_id(dim_2)

    dim_3 = qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension3", dim_def="Dim3",
                                        dim_label="'Dimension 3'", dim_desc="Dimension description 3",
                                        dim_tags=["dim3", "test"], dim_color="#8a85c6", single_color="#4477aa")
    dim_3_id = qixe.get_id(dim_3)


    ####################################################################################################################
    # Create sample master measures
    ####################################################################################################################

    gradient_measure_1 = qixe.structs.gradient(colors=["#ff0000", "#ffff00", "#00ff00"], break_types=[True, True],
                                               limits=[0.33, 0.66], limit_type="absolute")
    measure_1 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression1", mes_def="Sum(Expression1)",
                               mes_label="'Expression 1'", mes_desc="Expression description 1",
                               mes_tags=["exp1", "test"], mes_color="#332288", gradient=gradient_measure_1)
    measure_1_id = qixe.get_id(measure_1)

    measure_2 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression2", mes_def="Sum(Expression2)",
                               mes_label="'Expression 2'", mes_desc="Expression description 2",
                               mes_tags=["exp2", "test"], mes_color="#117733")
    measure_2_id = qixe.get_id(measure_2)

    gradient_measure_3 = qixe.structs.gradient(colors=["#00ff00", "#0000ff"])
    measure_3 = qixe.create_master_measure(app_handle=app_handle, mes_title="Expression3", mes_def="Sum(Expression3)",
                                           mes_label="'Expression 3'", mes_desc="Expression description 3",
                                           mes_tags=["exp3", "test"], gradient=gradient_measure_3)
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
    no_of_rows_sheet_4 = 42
    no_of_cols_sheet_4 = no_of_rows_sheet_4 * 2

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
    sheet_4 = qixe.create_sheet(app_handle=app_handle, sheet_title="My New Sheet 4", sheet_desc="Sheet description",
                                no_of_rows=no_of_rows_sheet_4)
    sheet_4_handle = qixe.get_handle(sheet_4)
    sheet_4_id = qixe.get_id(sheet_4)



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



    ####################################################################################################################
    # Create objects on sheet 3
    ####################################################################################################################

    # ------------------------------------------------------------------------------------------------------------------
    # Create filterpane
    # ------------------------------------------------------------------------------------------------------------------

    # Create filterpane frame
    filterpane_3 = qixe.create_filterpane_frame(handle=sheet_3_handle, no_of_rows_sheet=no_of_rows_sheet_3, col=0,
                                                row=0,
                                                colspan=no_of_cols_sheet_3, rowspan=3)
    filterpane_3_id = qixe.get_id(filterpane_3)

    # Create list objects
    filterpane_3_handle = qixe.get_handle(filterpane_3)
    qixe.create_list_object(handle=filterpane_3_handle, dim_id=dim_1_id, field_title="Dimension 1")
    qixe.create_list_object(handle=filterpane_3_handle, dim_id=dim_2_id, field_title="Dimension 2")
    qixe.create_list_object(handle=filterpane_3_handle, dim_id=dim_3_id, field_title="Dimension 3")
    qixe.create_list_object(handle=filterpane_3_handle, field_def="Alpha", field_title="Alpha")

    # ------------------------------------------------------------------------------------------------------------------
    # Create straight table
    # ------------------------------------------------------------------------------------------------------------------

    # Create the structure of tne dimensions
    sn_table_nx_inline_dimension_def_1 = qixe.structs.nx_inline_dimension_def()
    sn_table_nx_inline_dimension_def_2 = qixe.structs.nx_inline_dimension_def()
    sn_table_nx_inline_dimension_def_3 = qixe.structs.nx_inline_dimension_def()
    sn_table_hc_dim_1 = qixe.structs.nx_dimension(library_id=dim_1_id, dim_def=sn_table_nx_inline_dimension_def_1)
    sn_table_hc_dim_2 = qixe.structs.nx_dimension(library_id=dim_2_id, dim_def=sn_table_nx_inline_dimension_def_2)
    sn_table_hc_dim_3 = qixe.structs.nx_dimension(library_id=dim_3_id, dim_def=sn_table_nx_inline_dimension_def_3)
    sn_table_hc_dim_list = [sn_table_hc_dim_1, sn_table_hc_dim_2, sn_table_hc_dim_3]

    # Create the structure of tne measures
    sn_table_nx_inline_measure_def_1 = qixe.structs.nx_inline_measure_def()
    sn_table_nx_inline_measure_def_2 = qixe.structs.nx_inline_measure_def()
    sn_table_nx_inline_measure_def_3 = qixe.structs.nx_inline_measure_def()
    sn_table_hc_mes_1 = qixe.structs.nx_measure(library_id=measure_1_id, mes_def=sn_table_nx_inline_measure_def_1)
    sn_table_hc_mes_2 = qixe.structs.nx_measure(library_id=measure_2_id, mes_def=sn_table_nx_inline_measure_def_2)
    sn_table_hc_mes_3 = qixe.structs.nx_measure(library_id=measure_3_id, mes_def=sn_table_nx_inline_measure_def_3)
    sn_table_hc_mes_list = [sn_table_hc_mes_1, sn_table_hc_mes_2, sn_table_hc_mes_3]

    # Create hypercube structure for straight table
    hypercube_def_sn_table = qixe.structs.hypercube_def(dimensions=sn_table_hc_dim_list, measures=sn_table_hc_mes_list,
                                                     column_order=[0, 1, 2, 3, 4, 5],
                                                     column_widths=[-1, -1, -1, -1, -1, -1])

    # Create straight table
    sn_table_1 = qixe.create_chart(handle=sheet_3_handle, obj_type="sn-table", hypercube_def=hypercube_def_sn_table,
                                no_of_rows_sheet=no_of_rows_sheet_3, col=0, row=3, colspan=no_of_cols_sheet_3,
                                rowspan=no_of_rows_sheet_3 - 3)
    sn_table_1_id = qixe.get_id(sn_table_1)


    ####################################################################################################################
    # Create objects on sheet 4
    ####################################################################################################################

    # ------------------------------------------------------------------------------------------------------------------
    # Create filterpane 4
    # ------------------------------------------------------------------------------------------------------------------

    # Create filterpane frame
    filterpane_4 = qixe.create_filterpane_frame(handle=sheet_4_handle, no_of_rows_sheet=no_of_rows_sheet_4, col=0,
                                                row=0, colspan=no_of_cols_sheet_4, rowspan=3)
    filterpane_4_id = qixe.get_id(filterpane_4)

    # Create list objects
    filterpane_4_handle = qixe.get_handle(filterpane_4)
    qixe.create_list_object(handle=filterpane_4_handle, dim_id=dim_1_id, field_title="Dimension 1")
    qixe.create_list_object(handle=filterpane_4_handle, dim_id=dim_2_id, field_title="Dimension 2")
    qixe.create_list_object(handle=filterpane_4_handle, dim_id=dim_3_id, field_title="Dimension 3")
    qixe.create_list_object(handle=filterpane_4_handle, field_def="Alpha", field_title="Alpha")

    # ------------------------------------------------------------------------------------------------------------------
    # Create new pivot table
    # ------------------------------------------------------------------------------------------------------------------

    # Create the structure of tne dimensions
    sn_pivot_table_nx_inline_dimension_def_1 = qixe.structs.nx_inline_dimension_def()
    sn_pivot_table_nx_inline_dimension_def_2 = qixe.structs.nx_inline_dimension_def()
    sn_pivot_table_nx_inline_dimension_def_3 = qixe.structs.nx_inline_dimension_def()
    sn_pivot_table_hc_dim_1 = qixe.structs.nx_dimension(library_id=dim_1_id, dim_def=sn_pivot_table_nx_inline_dimension_def_1)
    sn_pivot_table_hc_dim_2 = qixe.structs.nx_dimension(library_id=dim_2_id, dim_def=sn_pivot_table_nx_inline_dimension_def_2)
    sn_pivot_table_hc_dim_3 = qixe.structs.nx_dimension(library_id=dim_3_id, dim_def=sn_pivot_table_nx_inline_dimension_def_3)
    sn_pivot_table_hc_dim_list = [sn_pivot_table_hc_dim_1, sn_pivot_table_hc_dim_2, sn_pivot_table_hc_dim_3]

    # Create the structure of tne measures
    sn_pivot_table_nx_inline_measure_def_1 = qixe.structs.nx_inline_measure_def()
    sn_pivot_table_nx_inline_measure_def_2 = qixe.structs.nx_inline_measure_def()
    sn_pivot_table_nx_inline_measure_def_3 = qixe.structs.nx_inline_measure_def()
    sn_pivot_table_hc_mes_1 = qixe.structs.nx_measure(library_id=measure_1_id, mes_def=sn_pivot_table_nx_inline_measure_def_1)
    sn_pivot_table_hc_mes_2 = qixe.structs.nx_measure(library_id=measure_2_id, mes_def=sn_pivot_table_nx_inline_measure_def_2)
    sn_pivot_table_hc_mes_3 = qixe.structs.nx_measure(library_id=measure_3_id, mes_def=sn_pivot_table_nx_inline_measure_def_3)
    sn_pivot_table_hc_mes_list = [sn_pivot_table_hc_mes_1, sn_pivot_table_hc_mes_2, sn_pivot_table_hc_mes_3]

    # Create hypercube structure for new pivot table
    hypercube_def_sn_pivot_table = qixe.structs.hypercube_def(dimensions=sn_pivot_table_hc_dim_list,
                                                           measures=sn_pivot_table_hc_mes_list,
                                                           inter_column_sort_order=[0, 1, 2, -1], mode="P")

    # Create new pivot table
    sn_pivot_table_1 = qixe.create_chart(handle=sheet_4_handle, obj_type="sn-pivot-table",
                                      hypercube_def=hypercube_def_sn_pivot_table,
                                      no_of_rows_sheet=no_of_rows_sheet_4, col=0, row=3, colspan=no_of_cols_sheet_4,
                                      rowspan=no_of_rows_sheet_4 - 3)
    sn_pivot_table_1_id = qixe.get_id(sn_pivot_table_1)


    ####################################################################################################################
    # Storytelling
    ####################################################################################################################

    # ------------------------------------------------------------------------------------------------------------------
    # Create story
    # ------------------------------------------------------------------------------------------------------------------

    story_properties = qixe.structs.story_properties(title="API generated story", description="This is the story!")
    story = qixe.eaa.create_object(doc_handle=app_handle, prop=story_properties)
    story_handle = qixe.get_handle(obj=story)

    # ------------------------------------------------------------------------------------------------------------------
    # Create slides
    # ------------------------------------------------------------------------------------------------------------------

    # slide properties
    slide_properties = qixe.structs.slide_properties()

    # Slide 1
    slide_1 = qixe.egoa.create_child(handle=story_handle, prop=slide_properties)
    slide_1_handle = qixe.get_handle(obj=slide_1)
    slide_1_id = qixe.get_id(obj=slide_1)

    # Slide 2
    slide_2 = qixe.egoa.create_child(handle=story_handle, prop=slide_properties)
    slide_2_handle = qixe.get_handle(obj=slide_2)
    slide_2_id = qixe.get_id(obj=slide_2)

    # Slide 3
    slide_3 = qixe.egoa.create_child(handle=story_handle, prop=slide_properties)
    slide_3_handle = qixe.get_handle(obj=slide_3)
    slide_3_id = qixe.get_id(obj=slide_3)

    # Slide 4
    slide_4 = qixe.egoa.create_child(handle=story_handle, prop=slide_properties)
    slide_4_handle = qixe.get_handle(obj=slide_4)
    slide_4_id = qixe.get_id(obj=slide_4)

    # Slide 5
    slide_5 = qixe.egoa.create_child(handle=story_handle, prop=slide_properties)
    slide_5_handle = qixe.get_handle(obj=slide_5)
    slide_5_id = qixe.get_id(obj=slide_5)

    # Slide 6
    slide_6 = qixe.egoa.create_child(handle=story_handle, prop=slide_properties)
    slide_6_handle = qixe.get_handle(obj=slide_6)
    slide_6_id = qixe.get_id(obj=slide_6)

    # ------------------------------------------------------------------------------------------------------------------
    # Create objects on slide 1
    # ------------------------------------------------------------------------------------------------------------------

    # Create Text title
    slide_1_slideitem_title_properties = qixe.structs.slideitem_text_properties(visualization_type="title",
                                                                                style_text="Slide title")
    slide_1_title = qixe.egoa.create_child(handle=slide_1_handle, prop=slide_1_slideitem_title_properties)

    # Create text paragraph
    slideitem_paragraph_properties = qixe.structs.slideitem_text_properties(visualization_type="paragraph",
                                                                            style_text="Lorem ipsum dolor sit amet, consetetur sadipscing elitr...",
                                                                            position_width="95.83334%",
                                                                            position_height="81.4814875%",
                                                                            position_top="14.81481%",
                                                                            position_left="2.08333%",
                                                                            ratio=False)
    paragraph = qixe.egoa.create_child(handle=slide_1_handle, prop=slideitem_paragraph_properties)

    # ------------------------------------------------------------------------------------------------------------------
    # Create objects on slide 2
    # ------------------------------------------------------------------------------------------------------------------

    # Create Text title
    slide_2_slideitem_title_properties = qixe.structs.slideitem_text_properties(visualization_type="title",
                                                                                style_text="Shapes 1")
    slide_2_title = qixe.egoa.create_child(handle=slide_2_handle, prop=slide_2_slideitem_title_properties)

    # Create square shape
    slideitem_square_properties = qixe.structs.slideitem_shape_properties(visualization_type="square",
                                                                         position_width="12.50000%",
                                                                         position_height="22.21840%",
                                                                         position_top="22.22222%",
                                                                         position_left="6.25000%")
    square = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_square_properties)

    # Create rounded square shape
    slideitem_square_rounded_properties = qixe.structs.slideitem_shape_properties(visualization_type="square_rounded",
                                                                                  position_width="12.50000%",
                                                                                  position_height="22.21840%",
                                                                                  position_top="22.22222%",
                                                                                  position_left="20.83333%")
    square_rounded = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_square_rounded_properties)

    # Create circle shape
    slideitem_circle_properties = qixe.structs.slideitem_shape_properties(visualization_type="circle",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="22.22222%",
                                                                           position_left="35.41667%")
    circle = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_circle_properties)

    # Create disc shape
    slideitem_disc_properties = qixe.structs.slideitem_shape_properties(visualization_type="disc",
                                                                          position_width="12.50000%",
                                                                          position_height="22.21840%",
                                                                          position_top="22.22222%",
                                                                          position_left="50.00000%")
    disc = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_disc_properties)

    # Create arrow (down) shape
    slideitem_arrow_d_properties = qixe.structs.slideitem_shape_properties(visualization_type="arrow_d",
                                                                        position_width="12.50000%",
                                                                        position_height="22.21840%",
                                                                        position_top="22.22222%",
                                                                        position_left="64.58333%")
    arrow_d = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_arrow_d_properties)

    # Create arrow (left) shape
    slideitem_arrow_l_properties = qixe.structs.slideitem_shape_properties(visualization_type="arrow_l",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="22.22222%",
                                                                           position_left="79.16667%")
    arrow_l = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_arrow_l_properties)

    # Create arrow (right) shape
    slideitem_arrow_r_properties = qixe.structs.slideitem_shape_properties(visualization_type="arrow_r",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="48.14815%",
                                                                           position_left="6.25000%")
    arrow_r = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_arrow_r_properties)

    # Create arrow (up) shape
    slideitem_arrow_u_properties = qixe.structs.slideitem_shape_properties(visualization_type="arrow_u",
                                                                                  position_width="12.50000%",
                                                                                  position_height="22.21840%",
                                                                                  position_top="48.14815%",
                                                                                  position_left="20.83333%")
    arrow_u = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_arrow_u_properties)

    # Create pullout (bellow) shape
    slideitem_pullout_b_properties = qixe.structs.slideitem_shape_properties(visualization_type="pullout_b",
                                                                          position_width="12.50000%",
                                                                          position_height="22.21840%",
                                                                          position_top="48.14815%",
                                                                          position_left="35.41667%")
    pullout_b = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_pullout_b_properties)

    # Create pullout (left) shape
    slideitem_pullout_l_properties = qixe.structs.slideitem_shape_properties(visualization_type="pullout_l",
                                                                        position_width="12.50000%",
                                                                        position_height="22.21840%",
                                                                        position_top="48.14815%",
                                                                        position_left="50.00000%")
    pullout_l = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_pullout_l_properties)

    # Create pullout (r) shape
    slideitem_pullout_r_properties = qixe.structs.slideitem_shape_properties(visualization_type="pullout_r",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="48.14815%",
                                                                           position_left="64.58333%")
    pullout_r = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_pullout_r_properties)

    # Create pullout (t) shape
    slideitem_pullout_t_properties = qixe.structs.slideitem_shape_properties(visualization_type="pullout_t",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="48.14815%",
                                                                           position_left="79.16667%")
    pullout_t = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_pullout_t_properties)

    # Create tri 1 shape
    slideitem_tri1_properties = qixe.structs.slideitem_shape_properties(visualization_type="tri1",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="74.07407%",
                                                                           position_left="6.25000%")
    tri1 = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_tri1_properties)

    # Create tri 2 shape
    slideitem_tri2_properties = qixe.structs.slideitem_shape_properties(visualization_type="tri2",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="74.07407%",
                                                                           position_left="20.83333%")
    tri2 = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_tri2_properties)

    # Create tri 3 shape
    slideitem_tri3_properties = qixe.structs.slideitem_shape_properties(visualization_type="tri3",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="74.07407%",
                                                                             position_left="35.41667%")
    tri3 = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_tri3_properties)

    # Create tri 4 shape
    slideitem_tri4_properties = qixe.structs.slideitem_shape_properties(visualization_type="tri4",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="74.07407%",
                                                                             position_left="50.00000%")
    tri4 = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_tri4_properties)

    # Create 2 lines (horizontal) shape
    slideitem_2lines_h_properties = qixe.structs.slideitem_shape_properties(visualization_type="2lines_h",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="74.07407%",
                                                                             position_left="64.58333%")
    line_h = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_2lines_h_properties)

    # Create 2 lines (vertical) shape
    slideitem_2lines_v_properties = qixe.structs.slideitem_shape_properties(visualization_type="2lines_v",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="74.07407%",
                                                                             position_left="79.16667%")
    line_v = qixe.egoa.create_child(handle=slide_2_handle, prop=slideitem_2lines_v_properties)

    # ------------------------------------------------------------------------------------------------------------------
    # Create objects on slide 3
    # ------------------------------------------------------------------------------------------------------------------

    # Create Text title
    slide_3_slideitem_title_properties = qixe.structs.slideitem_text_properties(visualization_type="title",
                                                                                style_text="Shapes 2")
    slide_3_title = qixe.egoa.create_child(handle=slide_3_handle, prop=slide_3_slideitem_title_properties)

    # Create plane shape
    slideitem_plane_properties = qixe.structs.slideitem_shape_properties(visualization_type="plane",
                                                                          position_width="12.50000%",
                                                                          position_height="22.21840%",
                                                                          position_top="22.22222%",
                                                                          position_left="6.25000%")
    plane = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_plane_properties)

    # Create bus shape
    slideitem_bus_properties = qixe.structs.slideitem_shape_properties(visualization_type="bus",
                                                                                  position_width="12.50000%",
                                                                                  position_height="22.21840%",
                                                                                  position_top="22.22222%",
                                                                                  position_left="20.83333%")
    bus = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_bus_properties)

    # Create car shape
    slideitem_car_properties = qixe.structs.slideitem_shape_properties(visualization_type="car",
                                                                          position_width="12.50000%",
                                                                          position_height="22.21840%",
                                                                          position_top="22.22222%",
                                                                          position_left="35.41667%")
    car = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_car_properties)

    # Create train shape
    slideitem_train_properties = qixe.structs.slideitem_shape_properties(visualization_type="train",
                                                                        position_width="12.50000%",
                                                                        position_height="22.21840%",
                                                                        position_top="22.22222%",
                                                                        position_left="50.00000%")
    train = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_train_properties)

    # Create dollar shape
    slideitem_dollar_properties = qixe.structs.slideitem_shape_properties(visualization_type="dollar",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="22.22222%",
                                                                           position_left="64.58333%")
    dollar = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_dollar_properties)

    # Create euro shape
    slideitem_euro_properties = qixe.structs.slideitem_shape_properties(visualization_type="euro",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="22.22222%",
                                                                           position_left="79.16667%")
    euro = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_euro_properties)

    # Create pound shape
    slideitem_pound_properties = qixe.structs.slideitem_shape_properties(visualization_type="pound",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="48.14815%",
                                                                           position_left="6.25000%")
    pound = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_pound_properties)

    # Create yen shape
    slideitem_yen_properties = qixe.structs.slideitem_shape_properties(visualization_type="yen",
                                                                           position_width="12.50000%",
                                                                           position_height="22.21840%",
                                                                           position_top="48.14815%",
                                                                           position_left="20.83333%")
    yen = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_yen_properties)

    # Create flag shape
    slideitem_flag_properties = qixe.structs.slideitem_shape_properties(visualization_type="flag",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="48.14815%",
                                                                             position_left="35.41667%")
    flag = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_flag_properties)

    # Create globe shape
    slideitem_globe_properties = qixe.structs.slideitem_shape_properties(visualization_type="globe",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="48.14815%",
                                                                             position_left="50.00000%")
    globe = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_globe_properties)

    # Create tree shape
    slideitem_tree_properties = qixe.structs.slideitem_shape_properties(visualization_type="tree",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="48.14815%",
                                                                             position_left="64.58333%")
    tree = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_tree_properties)

    # Create cloud shape
    slideitem_cloud_properties = qixe.structs.slideitem_shape_properties(visualization_type="cloud",
                                                                             position_width="12.50000%",
                                                                             position_height="22.21840%",
                                                                             position_top="48.14815%",
                                                                             position_left="79.16667%")
    cloud = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_cloud_properties)

    # Create light bulb shape
    slideitem_lightbulb_properties = qixe.structs.slideitem_shape_properties(visualization_type="lightbulb",
                                                                        position_width="12.50000%",
                                                                        position_height="22.21840%",
                                                                        position_top="74.07407%",
                                                                        position_left="6.25000%")
    lightbulb = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_lightbulb_properties)

    # Create clock shape
    slideitem_clock_properties = qixe.structs.slideitem_shape_properties(visualization_type="clock",
                                                                        position_width="12.50000%",
                                                                        position_height="22.21840%",
                                                                        position_top="74.07407%",
                                                                        position_left="20.83333%")
    clock = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_clock_properties)

    # Create man shape
    slideitem_man_properties = qixe.structs.slideitem_shape_properties(visualization_type="man",
                                                                        position_width="12.50000%",
                                                                        position_height="22.21840%",
                                                                        position_top="74.07407%",
                                                                        position_left="35.41667%")
    man = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_man_properties)

    # Create woman shape
    slideitem_woman_properties = qixe.structs.slideitem_shape_properties(visualization_type="woman",
                                                                        position_width="12.50000%",
                                                                        position_height="22.21840%",
                                                                        position_top="74.07407%",
                                                                        position_left="50.00000%")
    woman = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_woman_properties)

    # Create running man shape
    slideitem_running_man_properties = qixe.structs.slideitem_shape_properties(visualization_type="running_man",
                                                                            position_width="12.50000%",
                                                                            position_height="22.21840%",
                                                                            position_top="74.07407%",
                                                                            position_left="64.58333%")
    running_man = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_running_man_properties)

    # Create star shape
    slideitem_star_properties = qixe.structs.slideitem_shape_properties(visualization_type="star",
                                                                            position_width="12.50000%",
                                                                            position_height="22.21840%",
                                                                            position_top="74.07407%",
                                                                            position_left="79.16667%")
    star = qixe.egoa.create_child(handle=slide_3_handle, prop=slideitem_star_properties)

    # ------------------------------------------------------------------------------------------------------------------
    # Create objects on slide 4
    # ------------------------------------------------------------------------------------------------------------------

    # Create Text title
    slide_4_slideitem_title_properties = qixe.structs.slideitem_text_properties(visualization_type="title",
                                                                                style_text="Shapes 3")
    slide_4_title = qixe.egoa.create_child(handle=slide_4_handle, prop=slide_4_slideitem_title_properties)

    # Create tick shape
    slideitem_tick_properties = qixe.structs.slideitem_shape_properties(visualization_type="tick",
                                                                         position_width="12.50000%",
                                                                         position_height="22.21840%",
                                                                         position_top="22.22222%",
                                                                         position_left="6.25000%")
    tick = qixe.egoa.create_child(handle=slide_4_handle, prop=slideitem_tick_properties)

    # Create cross shape
    slideitem_cross_properties = qixe.structs.slideitem_shape_properties(visualization_type="cross",
                                                                       position_width="12.50000%",
                                                                       position_height="22.21840%",
                                                                       position_top="22.22222%",
                                                                       position_left="20.83333%")
    cross = qixe.egoa.create_child(handle=slide_4_handle, prop=slideitem_cross_properties)

    # Create banned shape
    slideitem_banned_properties = qixe.structs.slideitem_shape_properties(visualization_type="banned",
                                                                       position_width="12.50000%",
                                                                       position_height="22.21840%",
                                                                       position_top="22.22222%",
                                                                       position_left="35.41667%")
    banned = qixe.egoa.create_child(handle=slide_4_handle, prop=slideitem_banned_properties)

    # ------------------------------------------------------------------------------------------------------------------
    # Create objects on slide 5
    # ------------------------------------------------------------------------------------------------------------------

    # Create Text title
    slide_5_slideitem_title_properties = qixe.structs.slideitem_text_properties(visualization_type="title",
                                                                                style_text="Straight table")
    slide_5_title = qixe.egoa.create_child(handle=slide_5_handle, prop=slide_5_slideitem_title_properties)

    # Create snapshot
    snapshot_1 = qixe.create_snapshot(app_handle=app_handle, object_id=sn_table_1_id, snapshot_title="Straight table",
                                    snapshot_description="API generated snapshot")
    snapshot_1_id = qixe.get_id(snapshot_1)

    # Embed snapshot into slide 5
    qixe.embed_snapshot(app_handle=app_handle, snapshot_id=snapshot_1_id, slide_id=slide_5_id)

    # ------------------------------------------------------------------------------------------------------------------
    # Create objects on slide 6
    # ------------------------------------------------------------------------------------------------------------------

    # Create Text title
    slide_6_slideitem_title_properties = qixe.structs.slideitem_text_properties(visualization_type="title",
                                                                                style_text="Pivot table")
    slide_6_title = qixe.egoa.create_child(handle=slide_6_handle, prop=slide_6_slideitem_title_properties)

    # Create snapshot
    snapshot_2 = qixe.create_snapshot(app_handle=app_handle, object_id=pivot_table_1_id, snapshot_title="Pivot table",
                                      snapshot_description="API generated snapshot")
    snapshot_2_id = qixe.get_id(snapshot_2)

    # Embed snapshot into slide 6
    qixe.embed_snapshot(app_handle=app_handle, snapshot_id=snapshot_2_id, slide_id=slide_6_id)


    # Save app
    save_sample_app(qixe, app_handle)

    return (app_handle, dim_1_id, dim_2_id, dim_3_id, measure_1_id, measure_2_id, measure_3_id, sheet_1_id,
            filterpane_1_id, table_1_id, sheet_2_id, filterpane_2_id, pivot_table_1_id, sheet_3_id, filterpane_3_id,
            sn_table_1_id, sheet_4_id, filterpane_4_id, sn_pivot_table_1_id)


def save_sample_app(qixe, app_handle: int):
    qixe.eaa.do_save(app_handle, "TestApp")


def close_connection(qixe):
    # Import engine package
    from qe_api_client.engine import QixEngine

    QixEngine.disconnect(qixe)


def delete_sample_app(qixe):
    qixe.ega.delete_app("TestApp")
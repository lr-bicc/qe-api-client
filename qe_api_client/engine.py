import json

import qe_api_client.api_classes.engine_app_api as engine_app_api
import qe_api_client.engine_communicator as engine_communicator
import qe_api_client.api_classes.engine_field_api as engine_field_api
import qe_api_client.api_classes.engine_generic_object_api as engine_generic_object_api
import qe_api_client.api_classes.engine_global_api as engine_global_api
import qe_api_client.api_classes.engine_generic_variable_api as engine_generic_variable_api
import qe_api_client.api_classes.engine_generic_dimension_api as engine_generic_dimension_api
import qe_api_client.api_classes.engine_generic_measure_api as engine_generic_measure_api
import qe_api_client.structs as structs
import math
import pandas as pd
import numpy as np


class QixEngine:
    """
    The class of the client to interact with the Qlik Sense Engine API.

    Methods:
        select_in_dimension(app_handle, dimension_name, list_of_values): Selects values in a given field.
    """

    def __init__(self, url, user_directory=None, user_id=None, ca_certs=None, certfile=None, keyfile=None, app_id=None):
        self.url = url

        # Check, if server or local connection available
        if user_directory is None and user_id is None and ca_certs is None and certfile is None and keyfile is None:
            self.conn = engine_communicator.EngineCommunicator(url)
        else:
            self.conn = engine_communicator.SecureEngineCommunicator(url, user_directory, user_id, ca_certs, certfile,
                                                                     keyfile, app_id)

        self.ega = engine_global_api.EngineGlobalApi(self.conn)
        self.eaa = engine_app_api.EngineAppApi(self.conn)
        self.egoa = engine_generic_object_api.EngineGenericObjectApi(self.conn)
        self.efa = engine_field_api.EngineFieldApi(self.conn)
        self.egva = engine_generic_variable_api.EngineGenericVariableApi(self.conn)
        self.egda = engine_generic_dimension_api.EngineGenericDimensionApi(self.conn)
        self.egma = engine_generic_measure_api.EngineGenericMeasureApi(self.conn)
        self.structs = structs
        self.app_handle = ''

    def select_in_field(self, app_handle, field_name, list_of_values):
        lb_field = self.eaa.get_field(app_handle, field_name)
        fld_handle = self.get_handle(lb_field)
        if fld_handle is None:
            return "The field name " + field_name + " doesn't exist!"
        else:
            values_to_select = []
            for val in list_of_values:
                fld_value = self.structs.field_value(text=val)
                values_to_select.append(fld_value)
            return self.efa.select_values(fld_handle, values_to_select)

    def select_excluded_in_field(self, app_handle, field_name):
        lb_field = self.eaa.get_field(app_handle, field_name)
        fld_handle = self.get_handle(lb_field)
        return self.efa.select_excluded(fld_handle)

    def select_possible_in_field(self, app_handle, field_name):
        lb_field = self.eaa.get_field(app_handle, field_name)
        fld_handle = self.get_handle(lb_field)
        return self.efa.select_possible(fld_handle)

    # return a list of tuples where first value in tuple is the actual
    # data value and the second tuple value is that
    # values selection state
    def get_list_object_data(self, app_handle, field_name):
        lb_field = self.eaa.get_field(app_handle, field_name)
        fld_handle = self.get_handle(lb_field)

        nx_inline_dimension_def = self.structs.nx_inline_dimension_def([field_name])
        nx_page = self.structs.nx_page(left=0, top=0, width=self.efa.get_cardinal(fld_handle))
        lb_def = self.structs.list_object_def("$", "", nx_inline_dimension_def,
                                              [nx_page])

        # Create info structure
        nx_info = self.structs.nx_info(obj_type="ListObject", obj_id="SLB01")

        # Create generic object properties structure
        gen_obj_props = self.structs.generic_object_properties(info=nx_info, prop_name="qListObjectDef", prop_def=lb_def)
        listobj = self.eaa.create_session_object(app_handle, gen_obj_props)  # NOQA
        listobj_handle = self.get_handle(listobj)
        val_list = self.egoa.get_layout(listobj_handle)["qListObject"]["qDataPages"][0]["qMatrix"]  # NOQA
        val_n_state_list = []
        for val in val_list:
            val_n_state_list.append((val[0]["qText"], val[0]["qState"]))

        return val_n_state_list

    def clear_selection_in_dimension(self, app_handle, dimension_name):
        lb_field = self.eaa.get_field(app_handle, dimension_name)
        fld_handle = self.get_handle(lb_field)
        return self.efa.clear(fld_handle)


    def create_single_master_dimension(self, app_handle: int, dim_title: str, dim_def: str, dim_label: str = "",
                                       dim_desc: str = "", dim_tags: list = None, dim_color: str = None,
                                       dim_color_index: int = -1, value_colors: list = None,
                                       null_value_color: str = None, null_value_color_index: int = -1,
                                       other_value_color: str = None, other_value_color_index: int = -1,
                                       single_color: str = None, single_color_index: int = -1, palette: str = None
                                       ):
        """
        Creates a single master dimension.

        Parameters:
            app_handle (int): The handle of the app.
            dim_title (str): The title of the dimension.
            dim_def (str): The definition of the dimension.
            dim_label (str, optional): The label of the dimension.
            dim_desc (str, optional): The description of the dimension.
            dim_tags (list, optional): The tags of the dimension.
            dim_color (str, optional): The master dimension color.
            dim_color_index (int, optional): The index of the master dimension color in the theme color picker.
            value_colors (list, optional): The value colors of the master dimension.
            null_value_color (str, optional): The NULL value color of the master dimension.
            null_value_color_index (int, optional): The index of the NULL value color of the master dimension in the theme color picker.
            other_value_color (str, optional): The OTHER value color of the master dimension.
            other_value_color_index (int, optional): The index of the OTHER value color of the master dimension in the theme color picker.
            single_color (str, optional): Single color of the values of the master dimension.
            single_color_index (int, optional): The index of single color of the values of the master dimension in the theme color picker.
            palette (str, optional): Choose a color palette, if there are more than one.

        Returns:
            dict: The handle and Id of the dimension.
        """
        if value_colors is None:
            value_colors = []
        if dim_tags is None:
            dim_tags = []

        # Define of the single dimension properties
        nx_info = self.structs.nx_info(obj_type="dimension")
        if dim_color is None:
            coloring = self.structs.dim_coloring()
        else:
            coloring = self.structs.dim_coloring(base_color={"color": dim_color, "index": dim_color_index})

        nx_library_dimension_def = self.structs.nx_library_dimension_def(grouping="N", field_definitions=[dim_def],
                                                                         field_labels=[dim_title],
                                                                         label_expression=dim_label, alias=dim_title,
                                                                         title=dim_title, coloring=coloring)
        gen_dim_props = self.structs.generic_dimension_properties(nx_info=nx_info,
                                                                  nx_library_dimension_def=nx_library_dimension_def,
                                                                  title=dim_title, description=dim_desc, tags=dim_tags)

        # Create the single dimension
        master_dim = self.eaa.create_dimension(app_handle, gen_dim_props)

        # Get id and handle of the master dimension
        master_dim_id = self.get_id(master_dim)
        master_dim_handle = self.get_handle(master_dim)

        # Update "colorMapRef" property with the master dimension id.
        patch_value = json.dumps(master_dim_id)
        patch_color_map_ref = self.structs.nx_patch(op="replace", path="/qDim/coloring/colorMapRef", value=patch_value)
        self.egda.apply_patches(handle=master_dim_handle, patches=[patch_color_map_ref])

        # Define the color properties
        if null_value_color is None:
            null_value = None
        else:
            null_value = {"color": null_value_color, "index": null_value_color_index}

        if other_value_color is None:
            other_value = None
        else:
            other_value = {"color": other_value_color, "index": other_value_color_index}

        if single_color is None:
            single = None
        else:
            single = {"color": single_color, "index": single_color_index}

        colors = value_colors
        color_map = self.structs.color_map(colors=colors, nul=null_value, oth=other_value, single=single, pal=palette)
        color_map_props = self.structs.color_map_properties(dim_id=master_dim_id, _color_map=color_map)

        # Create color map object, if colors are passed.
        if value_colors or null_value_color is not None or other_value_color is not None or single_color is not None or palette is not None:
            color_map_model = self.eaa.create_object(app_handle, color_map_props)
            color_map_model_handle = self.get_handle(color_map_model)

            # Set "autoFill" and "usePal" to "False", if a single color is passed.
            if bool(single):
                patch_value_use_pal_auto_fill = json.dumps(False)
                patch_use_pal = self.structs.nx_patch(op="replace", path="/colorMap/usePal",
                                                      value=patch_value_use_pal_auto_fill)
                self.egda.apply_patches(handle=color_map_model_handle, patches=[patch_use_pal])

                patch_auto_fill = self.structs.nx_patch(op="replace", path="/colorMap/autoFill",
                                                      value=patch_value_use_pal_auto_fill)
                self.egda.apply_patches(handle=color_map_model_handle, patches=[patch_auto_fill])

            # Set "autoFill" to "False", if a color palette is passed.
            if palette is not None:
                patch_value_auto_fill = json.dumps(False)
                patch_auto_fill = self.structs.nx_patch(op="replace", path="/colorMap/autoFill",
                                                        value=patch_value_auto_fill)
                self.egda.apply_patches(handle=color_map_model_handle, patches=[patch_auto_fill])

        # Update "hasValueColors" property, if value colors are passed.
        if value_colors:
            patch_value_has_value_colors = json.dumps(True)
            patch_has_value_colors = self.structs.nx_patch(op="replace", path="/qDim/coloring/hasValueColors",
                                                        value=patch_value_has_value_colors)
            self.egda.apply_patches(handle=master_dim_handle, patches=[patch_has_value_colors])

        return master_dim


    def create_master_measure(self, app_handle: int, mes_title: str, mes_def: str, mes_label: str = "",
                              mes_desc: str = "", mes_tags: list = None, mes_color: str = None,
                              mes_color_index: int = -1, gradient: dict = None):
        """
        Creates a master measure.

        Parameters:
            app_handle (int): The handle of the app.
            mes_title (str): The title of the measure.
            mes_def (str): The definition of the measure.
            mes_label (str, optional): The label of the measure.
            mes_desc (str, optional): The description of the measure.
            mes_tags (list, optional): The tags of the measure.
            mes_color (str, optional): The color of the measure.
            mes_color_index (int, optional): The index of the color of the measure.

        Returns:
            dict: The handle and Id of the measure.
        """
        if mes_tags is None:
            mes_tags = []

        # Define of the measure properties
        nx_info = self.structs.nx_info(obj_type="measure")

        if mes_color is None:
            coloring = self.structs.mes_coloring()
        else:
            coloring = self.structs.mes_coloring(base_color={"color": mes_color, "index": mes_color_index})

        if gradient is not None:
            coloring.update({"gradient": gradient})

        nx_library_measure_def = self.structs.nx_library_measure_def(label=mes_title, mes_def=mes_def,
                                                                     label_expression=mes_label, coloring=coloring)
        gen_mes_props = self.structs.generic_measure_properties(nx_info=nx_info,
                                                                nx_library_measure_def=nx_library_measure_def,
                                                                title=mes_title, description=mes_desc, tags=mes_tags)

        # Create the measure
        master_mes = self.eaa.create_measure(app_handle, gen_mes_props)

        return master_mes

    def create_sheet(self, app_handle: int, sheet_title: str, sheet_desc: str = "", no_of_rows: int = 18):
        """
        Creates a sheet.

        Parameters:
            app_handle (int): The handle of the app.
            sheet_title (str): The title of the sheet.
            sheet_desc (str, optional): The description of the sheet.
            no_of_rows (int, optional): TThe number of the sheet rows. Min. 8 rows and max. 42 rows.

        Returns:
            dict: The handle and Id of the sheet.
        """
        # Define of the sheet properties
        nx_info = self.structs.nx_info(obj_type="sheet")
        sheet_def = {"title": sheet_title, "description": sheet_desc}
        sheet_props = self.structs.generic_object_properties(info=nx_info, prop_name="qMetaDef", prop_def=sheet_def)

        # Add row and column attributes. The number of the row should be between 8 and 42.
        if no_of_rows not in range(8, 43):
            no_of_rows = 18
        no_of_columns = no_of_rows * 2

        # Derive the grid_resolution property
        if no_of_rows == 12:
            grid_resolution = "small"
        elif no_of_rows == 15:
            grid_resolution = "medium"
        elif no_of_rows == 18:
            grid_resolution = "large"
        else:
            grid_resolution = "customrows"

        # Add new properties
        sheet_props.update(
            {
                "thumbnail": {"qStaticContentUrlDef": {"qUrl": ""}}, "columns": no_of_columns, "rows": no_of_rows,
                "customRowBase": no_of_rows, "gridResolution": grid_resolution, "layoutOptions": {"mobileLayout": "LIST"},
                "qChildListDef": {"qData": {"title": "/title"}}
            }
        )

        # Create the sheet
        sheet = self.eaa.create_object(app_handle, sheet_props)

        return sheet

    def create_list_object(self, handle: int, dim_id: str = "", field_def: str = "", field_title: str = ""):
        """
        Creates a list object.

        Parameters:
            handle (int): The handle of the parent object.
            dim_id (str, optional): The ID of the master dimension. Let this parameter empty, if you passed the "field_def".
            field_def (str, optional): The definition of the field. Let this parameter empty, if you passed the "dim_id".
            field_title (int, optional): The title of the field. Let this parameter empty, if you passed the "dim_id".

        Returns:
            dict: The handle and Id of the list object.
        """
        if field_def is None:
            field_def = []

        nx_info = self.structs.nx_info(obj_type="listbox")
        sort_criterias = self.structs.sort_criteria()

        nx_library_dimension_def = self.structs.nx_inline_dimension_def(grouping="N", field_definitions=[field_def],
                                                                          field_labels=[field_def],
                                                                          sort_criterias=[sort_criterias])
        list_object_def = self.structs.list_object_def(library_id=dim_id, definition=nx_library_dimension_def)
        list_object_props = self.structs.generic_object_properties(info=nx_info, prop_name="qListObjectDef",
                                                                   prop_def=list_object_def)
        list_object_props.update(
            {"showTitles": True, "title": field_title, "subtitle": "", "footnote": "", "disableNavMenu": False,
             "showDetails": True, "showDetailsExpression": False, "visualization": "listbox"})
        list_object = self.egoa.create_child(handle=handle, prop=list_object_props)

        return list_object

    def create_filterpane_frame(self, handle: int, no_of_rows_sheet: int, col: int, row: int, colspan: int, rowspan: int):
        """
        Creates a filterpane frame.

        Parameters:
            handle (int): The handle of the parent object.
            no_of_rows_sheet (int): The number of the sheet rows.
            col (int): First column the filterpane visualisation starts.
            row (int): First row the filterpane visualisation starts.
            colspan (int): The width of the filterpane in columns.
            rowspan (int): The height of the filterpane in rows.

        Returns:
            dict: The handle and Id of the filterpane frame.
        """
        nx_info = self.structs.nx_info(obj_type="filterpane")
        filterpane_props = self.structs.generic_object_properties(info=nx_info, prop_name="qMetaDef")
        filterpane_props.update({"qChildListDef": {"qData": {}}})
        filterpane = self.egoa.create_child(handle=handle, prop=filterpane_props)

        filterpane_id = self.get_id(filterpane)

        no_of_cols_sheet = no_of_rows_sheet * 2
        width = colspan / no_of_cols_sheet * 100
        height = rowspan / no_of_rows_sheet * 100
        y = row / no_of_rows_sheet * 100
        x = col / no_of_cols_sheet * 100

        if col >= 0 and colspan > 0 and no_of_cols_sheet >= col + colspan and row >= 0 and rowspan > 0 and no_of_rows_sheet >= row + rowspan:
            filterpane_layout = self.structs.object_position_size(obj_id=filterpane_id, obj_type="filterpane",
                                                                         col=col, row=row, colspan=colspan,
                                                                         rowspan=rowspan, y=y, x=x, width=width,
                                                                         height=height)

            sheet_layout = self.egoa.get_layout(handle=handle)

            if "cells" not in sheet_layout:
                patch_value = str([filterpane_layout]).replace("'", "\"")
                patch_cell = self.structs.nx_patch(op="add", path="/cells", value=patch_value)
            else:
                cells = sheet_layout["cells"]
                cells.append(filterpane_layout)
                patch_value = str(cells).replace("'", "\"")
                patch_cell = self.structs.nx_patch(op="replace", path="/cells", value=patch_value)

            self.egoa.apply_patches(handle=handle, patches=[patch_cell])
        else:
            print("The position of filterpane \"" + filterpane_id + "\" is out of range. This one will not be created.")

        return filterpane


    def create_chart(self, handle: int, obj_type: str, hypercube_def: dict, no_of_rows_sheet: int, col: int, row: int,
                     colspan: int, rowspan: int):
        """
        Creates a chart object.

        Parameters:
            handle (int): The handle of the parent object.
            obj_type (str): The type of the chart.
            hypercube_def (dict): Chart hypercube definition.
            no_of_rows_sheet (int): The number of the sheet rows.
            col (int): First column the chart visualisation starts.
            row (int): First row the chart visualisation starts.
            colspan (int): The width of the chart in columns.
            rowspan (int): The height of the chart in rows.

        Returns:
            dict: The handle and Id of the filterpane frame.
        """

        nx_info = self.structs.nx_info(obj_type=obj_type)
        if obj_type == "table":
            chart_props = self.structs.table_properties(info=nx_info, hypercube_def=hypercube_def)
        elif obj_type == "sn-table":
            chart_props = self.structs.sn_table_properties(info=nx_info, hypercube_def=hypercube_def)
        elif obj_type == "pivot-table":
            chart_props = self.structs.pivot_table_properties(info=nx_info, hypercube_def=hypercube_def)
        elif obj_type == "sn-pivot-table":
            chart_props = self.structs.pivot_table_properties(info=nx_info, hypercube_def=hypercube_def)
        else:
            print("Not valid object type.")

        chart = self.egoa.create_child(handle=handle, prop=chart_props)

        chart_id = self.get_id(chart)

        no_of_cols_sheet = no_of_rows_sheet * 2
        width = colspan / no_of_cols_sheet * 100
        height = rowspan / no_of_rows_sheet * 100
        y = row / no_of_rows_sheet * 100
        x = col / no_of_cols_sheet * 100

        if col >= 0 and colspan > 0 and no_of_cols_sheet >= col + colspan and row >= 0 and rowspan > 0 and no_of_rows_sheet >= row + rowspan:
            chart_layout = self.structs.object_position_size(obj_id=chart_id, obj_type=obj_type, col=col, row=row,
                                                             colspan=colspan, rowspan=rowspan, y=y, x=x, width=width,
                                                             height=height)

            sheet_layout = self.egoa.get_layout(handle=handle)

            if "cells" not in sheet_layout:
                patch_value = str([chart_layout]).replace("'", "\"")
                patch_cell = self.structs.nx_patch(op="add", path="/cells", value=patch_value)
            else:
                cells = sheet_layout["cells"]
                cells.append(chart_layout)
                patch_value = str(cells).replace("'", "\"")
                patch_cell = self.structs.nx_patch(op="replace", path="/cells", value=patch_value)

            self.egoa.apply_patches(handle=handle, patches=[patch_cell])
        else:
            print("The position of chart \"" + chart_id + "\" is out of range. This one will not be created.")

        return chart


    def get_app_lineage_info(self, app_handle):
        """
        Gets the lineage information of the app. The lineage information includes the LOAD and STORE statements from
        the data load script associated with this app.

        Parameters:
            app_handle (int): The handle of the app.

        Returns:
        DataFrame: Information about the lineage of the data in the app.
        """
        # Lineage-Daten aus der API holen
        lineage_info = self.eaa.get_lineage(app_handle)

        # Erstelle den DataFrame und fülle fehlende Werte mit ""
        df_lineage_info = pd.DataFrame(lineage_info)
        df_lineage_info = df_lineage_info[(df_lineage_info["qDiscriminator"].notna()) | (df_lineage_info["qStatement"].notna())].fillna("")
        return df_lineage_info

    def disconnect(self):
        self.conn.close_qvengine_connection(self.conn)

    @staticmethod
    def get_handle(obj):
        """
        Retrieves the handle from a given object.

        Parameters:
        obj : dict
            The object containing the handle.

        Returns:
        int: The handle value.

        Raises:
        ValueError: If the handle value is invalid.
        """
        try:
            return obj["qHandle"]
        except ValueError:
            return "Bad handle value in " + obj

    @staticmethod
    def get_id(obj):
        """
        Retrieves the id from a given object.

        Parameters:
        obj : dict
            The object containing the handle.

        Returns:
        int: The handle value.

        Raises:
        ValueError: If the handle value is invalid.
        """
        try:
            return obj["qGenericId"]
        except ValueError:
            return "Bad id value in " + obj

    def get_chart_data(self, app_handle, obj_id):
        """
        Retrieves the data from a given chart object.

        Parameters:
            app_handle (int): The handle of the app.
            obj_id (str): The ID of the chart object.

        Returns:
        DataFrame: A table of the chart content.
        """
        # Get object ID
        obj = self.eaa.get_object(app_handle, obj_id)
        if obj['qType'] is None:
            return 'Chart ID does not exists!'


        # Get object handle
        obj_handle = self.get_handle(obj)
        # Get object layout
        obj_layout = self.egoa.get_layout(obj_handle)

        # Determine the number of the columns and the rows the table has and splits in certain circumstances the table
        # calls
        no_of_columns = obj_layout['qHyperCube']['qSize']['qcx']

        if no_of_columns == 0:
            return 'The chart either contains no columns or has a calculation condition!'

        width = no_of_columns
        no_of_rows = obj_layout['qHyperCube']['qSize']['qcy']
        height = int(math.floor(10000 / no_of_columns))

        # Extract the dimension and measure titles and concat them to column names.
        dimension_info = obj_layout['qHyperCube'].get('qDimensionInfo', [])
        measure_info = obj_layout['qHyperCube'].get('qMeasureInfo', [])
        column_info = dimension_info + measure_info

        # Build the column mapping using qEffectiveInterColumnSortOrder
        sort_order = sorted(obj_layout['qHyperCube']['qEffectiveInterColumnSortOrder'])
        sort_order_positive = [x for x in sort_order if x >= 0]
        column_names = []
        for i in sort_order_positive:
            column_names.append(column_info[i]["qFallbackTitle"])

        # if the type of the charts has a straight data structure
        if (obj_layout['qInfo']['qType'] in ['table', 'sn-table', 'piechart', 'scatterplot', 'combochart', 'barchart']
                and obj_layout['qHyperCube']['qDataPages'] != []):

            # Paging variables
            page = 0
            data_values = []

            # Retrieves the hypercube data in a loop (because of limitation from 10.000 cells per call)
            while no_of_rows > page * height:
                nx_page = self.structs.nx_page(left=0, top=page * height, width=width, height=height)
                hc_data = self.egoa.get_hypercube_data(obj_handle, '/qHyperCubeDef', nx_page)[
                    'qDataPages'][0]['qMatrix']
                data_values.extend(hc_data)
                page += 1

            # Creates Dataframe from the content of the attribute 'qText'.
            df = pd.DataFrame([[d['qText'] for d in sublist] for sublist in data_values])

            # Assign titles zu Dataframe columns
            df.columns = column_names

        # if the type of the charts has a pivot data structure
        elif (obj_layout['qInfo']['qType'] in ['pivot-table', 'sn-pivot-table']
              and obj_layout['qHyperCube']['qPivotDataPages'] != []):

            # Supporting function to traverse all subnodes to get all dimensions
            def get_all_dimensions(node):
                label = node.get('qText', '')  # Leerer String, falls nicht vorhanden
                dimensions = [label]

                if 'qSubNodes' in node and node['qSubNodes']:
                    sub_dimensions = []
                    for sub_node in node['qSubNodes']:
                        sub_dimensions.extend([dimensions + d for d in get_all_dimensions(sub_node)])
                    return sub_dimensions
                else:
                    return [dimensions]

            # Supporting function to get all column headers for the pivot table
            def get_column_paths(node):
                label = node.get('qText', '')
                current_path = [label]

                if 'qSubNodes' in node and node['qSubNodes']:
                    paths = []
                    for sub in node['qSubNodes']:
                        for path in get_column_paths(sub):
                            paths.append(current_path + path)
                    return paths
                else:
                    return [current_path]

            col_headers = []
            nx_page_top = self.structs.nx_page(left=0, top=0, width=width, height=1)
            hc_top = self.egoa.get_hypercube_pivot_data(obj_handle, '/qHyperCubeDef', nx_page_top)['qDataPages'][0]['qTop']
            for top_node in hc_top:
                col_headers.extend(get_column_paths(top_node))

            # Paging variables
            page = 0
            row_headers = []
            data_values = []

            # Retrieves the hypercube data in a loop (bacause of limitation from 10.000 cells per call)
            while no_of_rows > page * height:
                nx_page = self.structs.nx_page(left=0, top=page * height, width=width, height=height)

                # Retrieves the row headers for the pivot table
                hc_left = self.egoa.get_hypercube_pivot_data(obj_handle, '/qHyperCubeDef', nx_page)[
                    'qDataPages'][0]['qLeft']
                for left_node in hc_left:
                    row_headers.extend(get_all_dimensions(left_node))

                # Retrieves the data for the pivot table
                hc_data = self.egoa.get_hypercube_pivot_data(obj_handle, '/qHyperCubeDef', nx_page)[
                    'qDataPages'][0]['qData']
                for row in hc_data:
                    data_values.append([cell['qText'] for cell in row])

                page += 1

            # Creates multi indes for rows and columns
            row_index = pd.MultiIndex.from_tuples(row_headers)
            col_index = pd.MultiIndex.from_tuples(col_headers)

            # Creates the Dataframe
            df = pd.DataFrame(data_values, index=row_index, columns=col_index)
            index_levels = df.index.nlevels
            df.index.names = column_names[:index_levels]
            df = df.reset_index()

        # if the type of the charts has a stacked data structure
        elif obj_layout['qInfo']['qType'] in ['barchart'] and obj_layout['qHyperCube']['qStackedDataPages'] != []:
            max_no_cells = no_of_columns * no_of_rows
            nx_page = self.structs.nx_page(left=0, top=0, width=no_of_columns, height=no_of_rows)
            hc_data = self.egoa.get_hypercube_stack_data(obj_handle, '/qHyperCubeDef', nx_page, max_no_cells)[
                'qDataPages'][0]['qData'][0]['qSubNodes']

            # Transform the nested structure into a flat DataFrame
            data_values = []
            for node in hc_data:
                for sub_node in node['qSubNodes']:
                    value = sub_node['qSubNodes'][0]['qValue'] if sub_node['qSubNodes'] else None
                    data_values.append([node['qText'], sub_node['qText'], value])

            # Creates the Dataframe
            df = pd.DataFrame(data_values, columns=column_names)

        else:
            return 'Chart type not supported.'

        # Returns the Dataframe
        return df

    def get_constructed_table_data(self, app_handle, list_of_dimensions = [], list_of_measures = [],
                                  list_of_master_dimensions = [], list_of_master_measures = []):
        """
        Creates a table from given fields, expressions, dimensions or measures and retrieves the data from it.

        Parameters:
            app_handle (int): The handle of the app.
            list_of_dimensions (list): A list of dimensions.
            list_of_measures (list): A list of measures.
            list_of_master_dimensions (list): A list of master dimensions.
            list_of_master_measures (list): A list of master measures.

        Returns:
            DataFrame: A table of the chart content.
        """
        # Create dimension property
        hc_dim = []
        for dimension in list_of_dimensions:
            hc_inline_dim_def = self.structs.nx_inline_dimension_def(field_definitions=[dimension])
            hc_dim.append(self.structs.nx_dimension(library_id="", dim_def=hc_inline_dim_def))
        for dimension in list_of_master_dimensions:
            hc_dim.append(self.structs.nx_dimension(library_id=dimension))

        # Create measure property
        hc_mes = []
        for measure in list_of_measures:
            hc_inline_mes = self.structs.nx_inline_measure_def(definition=measure)
            hc_mes.append(self.structs.nx_measure(library_id="", mes_def=hc_inline_mes))
        for measure in list_of_master_measures:
            hc_mes.append(self.structs.nx_measure(library_id=measure))

        # Create hypercube structure
        hc_def = self.structs.hypercube_def(state_name="$", dimensions=hc_dim, measures=hc_mes)

        # Create info structure
        nx_info = self.structs.nx_info(obj_type="table")

        # Create generic object properties structure
        gen_obj_props = self.structs.generic_object_properties(info=nx_info, prop_name="qHyperCubeDef", prop_def=hc_def)

        # Create session object
        hc_obj = self.eaa.create_session_object(app_handle, gen_obj_props)

        # Get object handle
        hc_obj_handle = self.get_handle(hc_obj)

        # Get object layout
        hc_obj_layout = self.egoa.get_layout(hc_obj_handle)

        # Determine the number of the columns and the rows the table has and splits in certain circumstances the table calls
        no_of_columns = hc_obj_layout['qHyperCube']['qSize']['qcx']
        width = no_of_columns
        no_of_rows = hc_obj_layout['qHyperCube']['qSize']['qcy']
        height = int(math.floor(10000 / no_of_columns))

        # Extract the dimension and measure titles and concat them to column names.
        dimension_titles = [dim['qFallbackTitle'] for dim in hc_obj_layout['qHyperCube']['qDimensionInfo']]
        measure_titles = [measure['qFallbackTitle'] for measure in hc_obj_layout['qHyperCube']['qMeasureInfo']]
        column_names = dimension_titles + measure_titles

        # Paging variables
        page = 0
        data_values = []

        # Retrieves the hypercube data in a loop (because of limitation from 10.000 cells per call)
        while no_of_rows > page * height:
            nx_page = self.structs.nx_page(left=0, top=page * height, width=width, height=height)
            hc_data = self.egoa.get_hypercube_data(hc_obj_handle, '/qHyperCubeDef', nx_page)['qDataPages'][0]['qMatrix']
            data_values.extend(hc_data)
            page += 1

        # Creates Dataframe from the content of the attribute 'qText'.
        df = pd.DataFrame([[d['qText'] for d in sublist] for sublist in data_values])

        # Assign titles zu Dataframe columns
        df.columns = column_names

        # Returns the Dataframe
        return df

    def get_apps(self):
        """
        Retrieves a list with all apps on the server containing metadata.

        Parameters:

        Returns:
            DataFrame: A table with all server apps.
        """

        # Get all apps from Qlik Server
        doc_list = self.ega.get_doc_list()

        # Convert into DataFrame structure
        df_doc_list = pd.DataFrame(doc_list)

        # Resolve the attribute "qMeta"
        field_meta = df_doc_list['qMeta'].apply(pd.Series).reindex(columns=["createdDate", "modifiedDate", "published",
                                                                            "publishTime", "privileges", "description",
                                                                            "qStaticByteSize", "dynamicColor", "create",
                                                                            "stream", "canCreateDataConnections"])

        # Concat the resolved attribute and rename the new columns
        df_doc_list_meta = pd.concat([df_doc_list.drop(['qMeta'], axis=1), field_meta], axis=1)
        df_doc_list_meta = df_doc_list_meta.rename(columns={"createdDate": "qMeta_createdDate",
                                                            "modifiedDate": "qMeta_modifiedDate",
                                                            "published": "qMeta_published",
                                                            "publishTime": "qMeta_publishTime",
                                                            "privileges": "qMeta_privileges",
                                                            "description": "qMeta_description",
                                                            "qStaticByteSize": "qMeta_qStaticByteSize",
                                                            "dynamicColor": "qMeta_dynamicColor",
                                                            "create": "qMeta_create",
                                                            "stream": "qMeta_stream",
                                                            "canCreateDataConnections": "qMeta_canCreateDataConnections"})

        # Resolve the attribute "stream"
        field_meta_stream = df_doc_list_meta['qMeta_stream'].apply(pd.Series).reindex(columns=["id", "name"])

        # Concat the resolved attribute and rename the new columns
        df_doc_list_meta_stream = pd.concat([df_doc_list_meta.drop(['qMeta_stream'], axis=1), field_meta_stream],
                                            axis=1)
        df_doc_list_meta_stream = df_doc_list_meta_stream.rename(
            columns={"id": "qMeta_stream_id", "name": "qMeta_stream_name"})

        # Resolve the attribute "qThumbnail"
        field_thumbnail = df_doc_list_meta_stream['qThumbnail'].apply(pd.Series).reindex(columns=["qUrl"])

        ## Concat the resolved attribute and rename the new columns
        df_doc_list_resolved = pd.concat([df_doc_list_meta_stream.drop(['qThumbnail'], axis=1), field_thumbnail],
                                         axis=1)
        df_doc_list_resolved = df_doc_list_resolved.rename(columns={"qUrl": "qThumbnail_qUrl"}).replace(np.nan,'')

        return df_doc_list_resolved


    def get_app_fields(self, app_handle):
        """
        Retrieves a list with all app fields containing meta data.

        Parameters:
            app_handle (int): The handle of the app.

        Returns:
            DataFrame: A table with all fields from an app.
        """
        # Define the parameters of the session object
        nx_info = self.structs.nx_info(obj_type="FieldList")
        field_list_def = self.structs.field_list_def()
        gen_obj_props = self.structs.generic_object_properties(info=nx_info, prop_name="qFieldListDef",
                                                               prop_def=field_list_def)

        # Create session object
        session = self.eaa.create_session_object(app_handle, gen_obj_props)

        # Get session handle
        session_handle = self.get_handle(session)

        # Get session object data
        layout = self.egoa.get_layout(session_handle)

        # Get the field list as Dictionary structure
        fields_list = layout["qFieldList"]["qItems"]

        # Define the DataFrame structure
        df_fields_list = pd.DataFrame(columns=['qIsHidden', 'qIsSystem', 'qName', 'qCardinal', 'qTags', 'qSrcTables'])

        for fields in fields_list:
            # Concatenate the field list on the DataFrame structure
            df_fields_list.loc[len(df_fields_list)] = fields

        return df_fields_list


    def get_app_dimensions(self, app_handle):
        """
        Retrieves a list with all app dimensions containing metadata.

        Parameters:
            app_handle (int): The handle of the app.

        Returns:
            DataFrame: A table with all dimensions from an app.
        """
        # Define the parameters of the session object
        nx_info = self.structs.nx_info(obj_type="DimensionList")
        dimension_list_def = self.structs.dimension_list_def()
        gen_obj_props = self.structs.generic_object_properties(info=nx_info, prop_name="qDimensionListDef",
                                                               prop_def=dimension_list_def)

        # Create session object
        session = self.eaa.create_session_object(app_handle, gen_obj_props)

        # Get session handle
        session_handle = self.get_handle(session)

        # Get session object data
        session_layout = self.egoa.get_layout(session_handle)

        # Get the dimension list as Dictionary structure
        dimension_list = session_layout["qDimensionList"]["qItems"]

        # Define the DataFrame structure
        df_dimension_list = pd.DataFrame(columns=["qInfo", "qMeta", "qDim", "qDimInfos"])

        for dimension in dimension_list:
            # Get dimension ID
            dim_id = dimension["qInfo"]["qId"]
            # Get dimension
            dim_result = self.egda.get_dimension(app_handle=app_handle, dimension_id=dim_id)
            # Get dimension handle
            dim_handle = self.get_handle(dim_result)
            # Get dimension metadata
            dim_layout = self.egoa.get_layout(dim_handle)

            # Concatenate the dimension to the DataFrame structure
            df_dimension_list.loc[len(df_dimension_list)] = dim_layout

        # Resolve the dictionary structure of attribute "qInfo"
        df_dimension_list_expanded = (df_dimension_list["qInfo"].dropna().apply(pd.Series).add_prefix("qInfo_"))
        df_dimension_list = df_dimension_list.drop(columns=["qInfo"]).join(df_dimension_list_expanded)

        # Resolve the dictionary structure of attribute "qMeta"
        df_dimension_list_expanded = (df_dimension_list["qMeta"].dropna().apply(pd.Series).add_prefix("qMeta_"))
        df_dimension_list = df_dimension_list.drop(columns=["qMeta"]).join(df_dimension_list_expanded)

        # Resolve the dictionary structure of attribute "qDim"
        df_dimension_list_expanded = (df_dimension_list["qDim"].dropna().apply(pd.Series).add_prefix("qDim_"))
        df_dimension_list = df_dimension_list.drop(columns=["qDim"]).join(df_dimension_list_expanded)

        # Resolve the dictionary structure of attribute "qDim_coloring"
        try:
            df_dimension_list_expanded = (
                df_dimension_list["qDim_coloring"].dropna().apply(pd.Series).add_prefix("qDim_coloring_"))
            df_dimension_list = df_dimension_list.drop(columns=["qDim_coloring"]).join(df_dimension_list_expanded)
        except KeyError:
            df_dimension_list["qDim_coloring"] = None

        # Resolve the dictionary structure of attribute "qDim_coloring_baseColor"
        try:
            df_dimension_list_expanded = (
                df_dimension_list["qDim_coloring_baseColor"].dropna().apply(pd.Series).add_prefix("qDim_coloring_baseColor_"))
            df_dimension_list = df_dimension_list.drop(columns=["qDim_coloring_baseColor"]).join(
                df_dimension_list_expanded)
        except KeyError:
            df_dimension_list["qDim_coloring_baseColor"] = None

        # Resolve the list structure of attribute
        df_dimension_list = df_dimension_list.explode(['qDimInfos', 'qDim_qFieldDefs', 'qDim_qFieldLabels'])

        # Resolve the dictionary structure of attribute "qDimInfos"
        df_dimension_list_expanded = (df_dimension_list["qDimInfos"].dropna().apply(pd.Series).add_prefix("qDimInfos_"))
        index = df_dimension_list_expanded.index
        df_dimension_list_expanded = df_dimension_list_expanded[~index.duplicated(keep="first")]
        df_dimension_list = df_dimension_list.drop(columns=["qDimInfos"]).join(df_dimension_list_expanded)

        return df_dimension_list


    def get_app_measures(self, app_handle):
        """
        Retrieves a list with all app measures containing metadata.

        Parameters:
            app_handle (int): The handle of the app.

        Returns:
            DataFrame: A table with all measures from an app.
        """
        # Define the parameters of the session object
        nx_info = self.structs.nx_info(obj_type="MeasureList")
        measure_list_def = self.structs.measure_list_def()
        gen_obj_props = self.structs.generic_object_properties(info=nx_info, prop_name="qMeasureListDef",
                                                               prop_def=measure_list_def)

        # Create session object
        session = self.eaa.create_session_object(app_handle, gen_obj_props)

        # Get session handle
        session_handle = self.get_handle(session)

        # Get session object data
        session_layout = self.egoa.get_layout(session_handle)

        # Get the measure list as Dictionary structure
        measure_list = session_layout["qMeasureList"]["qItems"]

        # Define the DataFrame structure
        df_measure_list = pd.DataFrame(columns=["qInfo", "qMeasure", "qMeta"])

        for measure in measure_list:
            # Get measure ID
            measure_id = measure["qInfo"]["qId"]
            # Get measure
            measure_result = self.egma.get_measure(app_handle=app_handle, measure_id=measure_id)
            # Get measure handle
            measure_handle = self.get_handle(measure_result)
            # Get session object data
            measure_layout = self.egoa.get_layout(measure_handle)

            # Concatenate the measure metadata to the DataFrame structure
            df_measure_list.loc[len(df_measure_list)] = measure_layout

        # Resolve the dictionary structure of attribute "qInfo"
        df_measure_list_expanded = (df_measure_list["qInfo"].dropna().apply(pd.Series).add_prefix("qInfo_"))
        df_measure_list = df_measure_list.drop(columns=["qInfo"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeasure"
        df_measure_list_expanded = (df_measure_list["qMeasure"].dropna().apply(pd.Series).add_prefix("qMeasure_"))
        df_measure_list = df_measure_list.drop(columns=["qMeasure"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeta"
        df_measure_list_expanded = (df_measure_list["qMeta"].apply(pd.Series).add_prefix("qMeta_"))
        df_measure_list = df_measure_list.drop(columns=["qMeta"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeasure_qNumFormat"
        df_measure_list_expanded = (
            df_measure_list["qMeasure_qNumFormat"].dropna().apply(pd.Series).add_prefix("qMeasure_qNumFormat_"))
        df_measure_list = df_measure_list.drop(columns=["qMeasure_qNumFormat"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeasure_coloring"
        try:
            df_measure_list_expanded = (
                df_measure_list["qMeasure_coloring"].dropna().apply(pd.Series).add_prefix("qMeasure_coloring_"))
            df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring"]).join(df_measure_list_expanded)
        except KeyError:
            df_measure_list["qMeasure_coloring"] = None

        # Resolve the dictionary structure of attribute "qMeasure_coloring_baseColor"
        try:
            df_measure_list_expanded = (df_measure_list["qMeasure_coloring_baseColor"].dropna().apply(pd.Series).add_prefix(
                "qMeasure_coloring_baseColor_"))
            df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring_baseColor"]).join(
                df_measure_list_expanded)
        except KeyError:
            df_measure_list["qMeasure_coloring_baseColor"] = None

        return df_measure_list


    def get_app_sheets(self, app_handle):
        """
        Retrieves a list with all app sheets and their content containing metadata.

        Parameters:
            app_handle (int): The handle of the app.

        Returns:
            DataFrame: A table with all sheets and their content from an app.
        """
        # Define the parameters of the session object
        nx_info = self.structs.nx_info(obj_type="SheetList")
        sheet_list_def = self.structs.sheet_list_def()
        gen_obj_props = self.structs.generic_object_properties(info=nx_info, prop_name="qAppObjectListDef",
                                                               prop_def=sheet_list_def)

        # Create session object
        session = self.eaa.create_session_object(app_handle, gen_obj_props)

        # Get session handle
        session_handle = self.get_handle(session)

        # Get session object data
        session_layout = self.egoa.get_layout(session_handle)

        # Get the sheet list as Dictionary structure
        sheet_list = session_layout["qAppObjectList"]["qItems"]

        # Define the DataFrame structure
        df_sheet_list = pd.DataFrame(columns=['qInfo', 'qMeta', 'qSelectionInfo', 'rank', 'thumbnail', 'columns', 'rows', 'cells', 'qChildList', 'gridResolution', 'layoutOptions', 'gridMode', 'customRowBase'])

        for sheet in sheet_list:
            # Get sheet ID
            sheet_id = sheet["qInfo"]["qId"]
            # Get sheet
            sheet_result = self.eaa.get_object(app_handle=app_handle, object_id=sheet_id)
            # Get sheet handle
            sheet_handle = self.get_handle(sheet_result)
            # Get session object data
            sheet_layout = self.egoa.get_layout(sheet_handle)

            # Concatenate the measure metadata to the DataFrame structure
            df_sheet_list.loc[len(df_sheet_list)] = sheet_layout

        # Resolve the dictionary structure of attribute "qInfo"
        df_sheet_list_expanded = (df_sheet_list["qInfo"].dropna().apply(pd.Series).add_prefix("qInfo_"))
        df_sheet_list = df_sheet_list.drop(columns=["qInfo"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "qMeta"
        df_sheet_list_expanded = (df_sheet_list["qMeta"].dropna().apply(pd.Series).add_prefix("qMeta_"))
        df_sheet_list = df_sheet_list.drop(columns=["qMeta"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "qSelectionInfo"
        df_sheet_list["qSelectionInfo"] = df_sheet_list["qSelectionInfo"].apply(
            lambda x: None if isinstance(x, dict) and len(x) == 0 else x
        )
        df_sheet_list_expanded = (df_sheet_list["qSelectionInfo"].dropna().apply(pd.Series).add_prefix("qSelectionInfo_"))
        df_sheet_list = df_sheet_list.drop(columns=["qSelectionInfo"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "thumbnail"
        df_sheet_list_expanded = (df_sheet_list["thumbnail"].dropna().apply(pd.Series).add_prefix("thumbnail_"))
        df_sheet_list = df_sheet_list.drop(columns=["thumbnail"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "thumbnail_qStaticContentUrl"
        df_sheet_list["thumbnail_qStaticContentUrl"] = df_sheet_list["thumbnail_qStaticContentUrl"].apply(
            lambda x: None if isinstance(x, dict) and len(x) == 0 else x
        )
        df_sheet_list_expanded = (df_sheet_list["thumbnail_qStaticContentUrl"].dropna().apply(pd.Series).add_prefix("thumbnail_qStaticContentUrl_"))
        df_sheet_list = df_sheet_list.drop(columns=["thumbnail_qStaticContentUrl"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "qChildList"
        df_sheet_list_expanded = (df_sheet_list["qChildList"].dropna().apply(pd.Series).add_prefix("qChildList_"))
        df_sheet_list = df_sheet_list.drop(columns=["qChildList"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "layoutOptions"
        df_sheet_list_expanded = (df_sheet_list["layoutOptions"].dropna().apply(pd.Series).add_prefix("layoutOptions_"))
        df_sheet_list = df_sheet_list.drop(columns=["layoutOptions"]).join(df_sheet_list_expanded)

        # Resolve the list structure of attribute
        df_sheet_list = df_sheet_list.explode(['cells', 'qChildList_qItems'])

        # Resolve the dictionary structure of attribute "cells"
        df_sheet_list_expanded = (df_sheet_list["cells"].dropna().apply(pd.Series).add_prefix("cells_"))
        index = df_sheet_list_expanded.index
        df_sheet_list_expanded = df_sheet_list_expanded[~index.duplicated(keep="first")]
        df_sheet_list = df_sheet_list.drop(columns=["cells"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "cells_bounds"
        df_sheet_list_expanded = (
            df_sheet_list["cells_bounds"].dropna().apply(pd.Series).add_prefix("cells_bounds_"))
        index = df_sheet_list_expanded.index
        df_sheet_list_expanded = df_sheet_list_expanded[~index.duplicated(keep="first")]
        df_sheet_list = df_sheet_list.drop(columns=["cells_bounds"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "qChildList_qItems"
        df_sheet_list_expanded = (
            df_sheet_list["qChildList_qItems"].dropna().apply(pd.Series).add_prefix("qChildList_qItems_"))
        index = df_sheet_list_expanded.index
        df_sheet_list_expanded = df_sheet_list_expanded[~index.duplicated(keep="first")]
        df_sheet_list = df_sheet_list.drop(columns=["qChildList_qItems"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "qChildList_qItems_qInfo"
        df_sheet_list_expanded = (
            df_sheet_list["qChildList_qItems_qInfo"].dropna().apply(pd.Series).add_prefix("qChildList_qItems_qInfo_"))
        index = df_sheet_list_expanded.index
        df_sheet_list_expanded = df_sheet_list_expanded[~index.duplicated(keep="first")]
        df_sheet_list = df_sheet_list.drop(columns=["qChildList_qItems_qInfo"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "qChildList_qItems_qMeta"
        df_sheet_list_expanded = (
            df_sheet_list["qChildList_qItems_qMeta"].dropna().apply(pd.Series).add_prefix("qChildList_qItems_qMeta_"))
        index = df_sheet_list_expanded.index
        df_sheet_list_expanded = df_sheet_list_expanded[~index.duplicated(keep="first")]
        df_sheet_list = df_sheet_list.drop(columns=["qChildList_qItems_qMeta"]).join(df_sheet_list_expanded)

        # Resolve the dictionary structure of attribute "qChildList_qItems_qData"
        df_sheet_list_expanded = (
            df_sheet_list["qChildList_qItems_qData"].dropna().apply(pd.Series).add_prefix("qChildList_qItems_qData_"))
        index = df_sheet_list_expanded.index
        df_sheet_list_expanded = df_sheet_list_expanded[~index.duplicated(keep="first")]
        df_sheet_list = df_sheet_list.drop(columns=["qChildList_qItems_qData"]).join(df_sheet_list_expanded)

        return df_sheet_list


    def get_app_variables(self, app_handle):
        """
        Retrieves a list with all app variables containing metadata.

        Parameters:
            app_handle (int): The handle of the app.

        Returns:
            DataFrame: A table with all variables from an app.
        """
        # Define the parameters of the session object
        nx_info = self.structs.nx_info(obj_type="VariableList")
        variable_list_def = self.structs.variable_list_def()
        gen_obj_props = self.structs.generic_object_properties(info=nx_info, prop_name="qVariableListDef",
                                                               prop_def=variable_list_def)

        # Create session object
        session = self.eaa.create_session_object(app_handle, gen_obj_props)

        # Get session handle
        session_handle = self.get_handle(session)

        # Get session object data
        session_layout = self.egoa.get_layout(session_handle)

        # Get the variable list as Dictionary structure
        variable_list = session_layout["qVariableList"]["qItems"]

        # Define the DataFrame structure
        df_variable_list = pd.DataFrame(columns=["qName", "qDefinition", "qMeta", "qInfo", "qData", "qIsScriptCreated", "qIsReserved"])

        for variable in variable_list:
            # Concatenate the measure metadata to the DataFrame structure
            df_variable_list.loc[len(df_variable_list)] = variable

        # Resolve the dictionary structure of attribute "qInfo"
        df_variable_list_expanded = (df_variable_list["qInfo"].dropna().apply(pd.Series).add_prefix("qInfo_"))
        df_variable_list = df_variable_list.drop(columns=["qInfo"]).join(df_variable_list_expanded)

        # Resolve the dictionary structure of attribute "qMeta"
        df_variable_list_expanded = (df_variable_list["qMeta"].dropna().apply(pd.Series).add_prefix("qMeta_"))
        df_variable_list = df_variable_list.drop(columns=["qMeta"]).join(df_variable_list_expanded)

        # Resolve the dictionary structure of attribute "qData"
        df_variable_list_expanded = (df_variable_list["qData"].dropna().apply(pd.Series).add_prefix("qData_"))
        df_variable_list = df_variable_list.drop(columns=["qData"]).join(df_variable_list_expanded)

        return df_variable_list


    def get_app_lineage(self, app_handle):
        """
        Retrieves a list with an app lineage data.

        Parameters:
            app_handle (int): The handle of the app.

        Returns:
            DataFrame: A table with lineage data from an app.
        """
        # Get lineage data from an app
        lineage_list = self.eaa.get_lineage(app_handle)

        # Define the DataFrame structure
        df_lineage_list = pd.DataFrame(columns=['qDiscriminator', 'qStatement'])

        for lineage in lineage_list:
            # Concatenate the lineage row on the DataFrame structure
            df_lineage_list.loc[len(df_lineage_list)] = lineage

        return df_lineage_list
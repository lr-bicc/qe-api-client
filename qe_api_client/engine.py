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
                                       dim_desc: str = "", dim_tags: list = None):
        """
        Creates a single master dimension.

        Parameters:
            app_handle (int): The handle of the app.
            dim_title (str): The title of the dimension.
            dim_def (str): The definition of the dimension.
            dim_label (str, optional): The label of the dimension.
            dim_desc (str, optional): The description of the dimension.
            dim_tags (list, optional): The tags of the dimension.

        Returns:
            dict: The handle and Id of the dimension.
        """
        if dim_tags is None:
            dim_tags = []
        nx_info = self.structs.nx_info(obj_type="dimension")
        nx_library_dimension_def = self.structs.nx_library_dimension_def(grouping="N", field_definitions=[dim_def],
                                                                         field_labels=[dim_title],
                                                                         label_expression=dim_label)
        gen_dim_props = self.structs.generic_dimension_properties(nx_info=nx_info,
                                                                  nx_library_dimension_def=nx_library_dimension_def,
                                                                  title=dim_title, description=dim_desc, tags=dim_tags)
        master_dim = self.eaa.create_dimension(app_handle, gen_dim_props)
        return master_dim

    def create_master_measure(self, app_handle: int, mes_title: str, mes_def: str, mes_label: str = "",
                              mes_desc: str = "", mes_tags: list = None):
        """
        Creates a master measure.

        Parameters:
            app_handle (int): The handle of the app.
            mes_title (str): The title of the measure.
            mes_def (str): The definition of the measure.
            mes_label (str, optional): The label of the measure.
            mes_desc (str, optional): The description of the measure.
            mes_tags (list, optional): The tags of the measure.

        Returns:
            dict: The handle and Id of the measure.
        """
        if mes_tags is None:
            mes_tags = []
        nx_info = self.structs.nx_info(obj_type="measure")
        nx_library_measure_def = self.structs.nx_library_measure_def(label=mes_title, mes_def=mes_def,
                                                                     label_expression=mes_label)
        gen_mes_props = self.structs.generic_measure_properties(nx_info=nx_info,
                                                                nx_library_measure_def=nx_library_measure_def,
                                                                title=mes_title, description=mes_desc, tags=mes_tags)
        master_mes = self.eaa.create_measure(app_handle, gen_mes_props)
        return master_mes

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
        width = no_of_columns
        no_of_rows = obj_layout['qHyperCube']['qSize']['qcy']
        height = int(math.floor(10000 / no_of_columns))

        # Extract the dimension and measure titles and concat them to column names.
        dimension_titles = [dim['qFallbackTitle'] for dim in obj_layout['qHyperCube']['qDimensionInfo']]
        measure_titles = [measure['qFallbackTitle'] for measure in obj_layout['qHyperCube']['qMeasureInfo']]
        column_names = dimension_titles + measure_titles

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
                dimensions = [node['qText']]
                # if 'qSubNodes' in node and node['qSubNodes']:
                if node['qSubNodes']:
                    sub_dimensions = []
                    for sub_node in node['qSubNodes']:
                        sub_dimensions.extend([dimensions + d for d in get_all_dimensions(sub_node)])
                    return sub_dimensions
                else:
                    return [dimensions]

            # Gets the column headers for the pivot table
            col_headers = []
            nx_page_top = self.structs.nx_page(left=0, top=0, width=width, height=1)
            hc_top = self.egoa.get_hypercube_pivot_data(obj_handle, '/qHyperCubeDef', nx_page_top)[
                'qDataPages'][0]['qTop']
            for top_node in hc_top:
                col_headers.extend(get_all_dimensions(top_node))

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
        hc_def = self.structs.hypercube_def(state_name="$", nx_dims=hc_dim, nx_meas=hc_mes)

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
        df_dimension_list_expanded = (df_dimension_list["qInfo"].apply(pd.Series).add_prefix("qInfo_"))
        df_dimension_list = df_dimension_list.drop(columns=["qInfo"]).join(df_dimension_list_expanded)

        # Resolve the dictionary structure of attribute "qMeta"
        df_dimension_list_expanded = (df_dimension_list["qMeta"].apply(pd.Series).add_prefix("qMeta_"))
        df_dimension_list = df_dimension_list.drop(columns=["qMeta"]).join(df_dimension_list_expanded)

        # Resolve the dictionary structure of attribute "qDim"
        df_dimension_list_expanded = (df_dimension_list["qDim"].apply(pd.Series).add_prefix("qDim_"))
        df_dimension_list = df_dimension_list.drop(columns=["qDim"]).join(df_dimension_list_expanded)

        # Resolve the dictionary structure of attribute "qDim_coloring"
        try:
            df_dimension_list_expanded = (
                df_dimension_list["qDim_coloring"].apply(pd.Series).add_prefix("qDim_coloring_"))
            df_dimension_list = df_dimension_list.drop(columns=["qDim_coloring"]).join(df_dimension_list_expanded)
        except KeyError:
            df_dimension_list["qDim_coloring"] = ""

        # Resolve the dictionary structure of attribute "qDim_coloring_baseColor"
        try:
            df_dimension_list_expanded = (
                df_dimension_list["qDim_coloring_baseColor"].apply(pd.Series).add_prefix("qDim_coloring_baseColor_"))
            df_dimension_list = df_dimension_list.drop(columns=["qDim_coloring_baseColor"]).join(
                df_dimension_list_expanded)
        except KeyError:
            df_dimension_list["qDim_coloring_baseColor"] = ""

        # Resolve the list structure of attribute
        df_dimension_list = df_dimension_list.explode(['qDimInfos', 'qDim_qFieldDefs', 'qDim_qFieldLabels'])

        # Resolve the dictionary structure of attribute "qDimInfos"
        df_dimension_list_expanded = (df_dimension_list["qDimInfos"].apply(pd.Series).add_prefix("qDimInfos_"))
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
        df_measure_list_expanded = (df_measure_list["qInfo"].apply(pd.Series).add_prefix("qInfo_"))
        df_measure_list = df_measure_list.drop(columns=["qInfo"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeasure"
        df_measure_list_expanded = (df_measure_list["qMeasure"].apply(pd.Series).add_prefix("qMeasure_"))
        df_measure_list = df_measure_list.drop(columns=["qMeasure"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeta"
        df_measure_list_expanded = (df_measure_list["qMeta"].apply(pd.Series).add_prefix("qMeta_"))
        df_measure_list = df_measure_list.drop(columns=["qMeta"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeasure_qNumFormat"
        df_measure_list_expanded = (
            df_measure_list["qMeasure_qNumFormat"].apply(pd.Series).add_prefix("qMeasure_qNumFormat_"))
        df_measure_list = df_measure_list.drop(columns=["qMeasure_qNumFormat"]).join(df_measure_list_expanded)

        # Resolve the dictionary structure of attribute "qMeasure_coloring"
        try:
            df_measure_list_expanded = (
                df_measure_list["qMeasure_coloring"].apply(pd.Series).add_prefix("qMeasure_coloring_"))
            df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring"]).join(df_measure_list_expanded)
        except KeyError:
            df_measure_list["qMeasure_coloring"] = ""

        # Resolve the dictionary structure of attribute "qMeasure_coloring_baseColor"
        try:
            df_measure_list_expanded = (df_measure_list["qMeasure_coloring_baseColor"].apply(pd.Series).add_prefix(
                "qMeasure_coloring_baseColor_"))
            df_measure_list = df_measure_list.drop(columns=["qMeasure_coloring_baseColor"]).join(
                df_measure_list_expanded)
        except KeyError:
            df_measure_list["qMeasure_coloring_baseColor"] = ""

        return df_measure_list


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
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


class QixEngine:

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

    def create_app(self, app_name='my_app'):
        app = self.ega.create_app(app_name)
        try:
            return app['qAppId']
        except KeyError:
            return app['message']

    def load_script(self, script):
        self.eaa.set_script(self.app_handle, script)
        return self.eaa.do_reload_ex(self.app_handle)['qResult']['qSuccess']

    def open_app(self, app_obj):
        opened_app = self.ega.open_doc(app_obj)
        self.app_handle = self.ega.get_handle(opened_app)
        return opened_app['qGenericId']

    def select_in_dimension(self, dimension_name, list_of_values):
        lb_field = self.eaa.get_field(self.app_handle, dimension_name)
        fld_handle = self.ega.get_handle(lb_field)
        values_to_select = []
        for val in list_of_values:
            val = {'qText': val}
            values_to_select.append(val)
        return self.efa.select_values(fld_handle, values_to_select)

    def select_excluded_in_dimension(self, dimension_name):
        lb_field = self.eaa.get_field(self.app_handle, dimension_name)
        fld_handle = self.ega.get_handle(lb_field)
        return self.efa.select_excluded(fld_handle)

    def select_possible_in_dimension(self, dimension_name):
        lb_field = self.eaa.get_field(self.app_handle, dimension_name)
        fld_handle = self.ega.get_handle(lb_field)
        return self.efa.select_possible(fld_handle)

    # return a list of tuples where first value in tuple is the actual
    # data value and the second tuple value is that
    # values selection state
    def get_list_object_data(self, dimension_name):
        lb_field = self.eaa.get_field(self.app_handle, dimension_name)
        fld_handle = self.ega.get_handle(lb_field)
        nx_page = self.structs.nx_page(0, 0, self.efa.get_cardinal(fld_handle)["qReturn"])
        lb_def = self.structs.list_object_def("$", "",[dimension_name], None,
                                              None, [nx_page])
        lb_param = {"qInfo": {"qId": "SLB01", "qType": "ListObject"}, "qListObjectDef": lb_def}
        listobj_handle = self.eaa.create_session_object(self.app_handle, lb_param)["qHandle"]  # NOQA
        val_list = self.egoa.get_layout(listobj_handle)["qListObject"]["qDataPages"][0]["qMatrix"]  # NOQA
        val_n_state_list = []
        for val in val_list:
            val_n_state_list.append((val[0]["qText"], val[0]["qState"]))
        return val_n_state_list

    def clear_selection_in_dimension(self, dimension_name):
        lb_field = self.eaa.get_field(self.app_handle, dimension_name)
        fld_handle = self.ega.get_handle(lb_field)
        return self.efa.clear(fld_handle)['qReturn']

    def clear_all_selections(self):
        return self.eaa.clear_all(self.app_handle, True)

    def delete_app(self, app_name):
        return self.ega.delete_app(app_name)['qSuccess']

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
                nx_page = self.structs.nx_page(0, page * height, width, height)
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
            nx_page_top = self.structs.nx_page(0, 0, width, 1)
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
                nx_page = self.structs.nx_page(0, page * height, width, height)

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
            nx_page = self.structs.nx_page(0, 0, no_of_columns, no_of_rows)
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
            hc_inline_dim_def = self.structs.nx_inline_dimension_def([dimension])
            hc_dim.append(self.structs.nx_dimension("", hc_inline_dim_def))
        for dimension in list_of_master_dimensions:
            hc_dim.append(self.structs.nx_dimension(dimension))

        # Create measure property
        hc_mes = []
        for measure in list_of_measures:
            hc_inline_mes = self.structs.nx_inline_measure_def(measure)
            hc_mes.append(self.structs.nx_measure("", hc_inline_mes))
        for measure in list_of_master_measures:
            hc_mes.append(self.structs.nx_measure(measure))

        # Create hypercube structure
        hc_def = self.structs.hypercube_def("$", hc_dim, hc_mes)

        # Create info structure
        nx_info = self.structs.nx_info("table")

        # Create generic object properties structure
        gen_obj_props = self.structs.generic_object_properties(nx_info, "qHyperCubeDef", hc_def)

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
            nx_page = self.structs.nx_page(0, page * height, width, height)
            hc_data = self.egoa.get_hypercube_data(hc_obj_handle, '/qHyperCubeDef', nx_page)['qDataPages'][0]['qMatrix']
            data_values.extend(hc_data)
            page += 1

        # Creates Dataframe from the content of the attribute 'qText'.
        df = pd.DataFrame([[d['qText'] for d in sublist] for sublist in data_values])

        # Assign titles zu Dataframe columns
        df.columns = column_names

        # Returns the Dataframe
        return df
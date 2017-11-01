import engine_communicator
import engine_global_api
import engine_app_api
import engine_generic_object_api
import engine_field_api
import structs


class QixEngine:

    def __init__(self, url):
        self.url = url
        self.conn = engine_communicator.EngineCommunicator(url)
        self.ega = engine_global_api.EngineGlobalApi(self.conn)
        self.eaa = engine_app_api.EngineAppApi(self.conn)
        self.egoa = engine_generic_object_api.EngineGenericObjectApi(self.conn)
        self.efa = engine_field_api.EngineFieldApi(self.conn)
        self.Structs = structs.Structs()
        self.app_handle = ''

    def create_app(self, app_name='my_app'):
        app = self.ega.create_app(app_name)
        return app['qAppId']

    def load_script(self, script):
        self.eaa.set_script(self.app_handle, script)
        return self.eaa.do_reload_ex(self.app_handle)['qSuccess']

    def open_app(self, app_obj):
        opened_app = self.ega.open_doc(app_obj)
        self.app_handle = self.ega.get_handle(opened_app)
        return opened_app['qGenericId']

    def create_hypercube(self, list_of_dimensions=[], list_of_measures=[], rows_to_return=1000):
        no_of_columns = len(list_of_dimensions) + len(list_of_measures)
        hc_dim = []
        for d in list_of_dimensions:
            hc_inline_dim = self.Structs.nx_inline_dimension_def([d])
            hc_dim.append(self.Structs.nx_hypercube_dimensions(hc_inline_dim))
        hc_mes = []
        for m in list_of_measures:
            hc_mes_sort = self.Structs.nx_sort_by()
            hc_inline_mes = self.Structs.nx_inline_measure_def(m)
            hc_mes.append(self.Structs.nx_hypercube_measure(hc_mes_sort, hc_inline_mes))
        nx_page = self.Structs.nx_page(0, 0, rows_to_return, no_of_columns)
        hc_def = self.Structs.hypercube_def("$", hc_dim, hc_mes, [nx_page])
        hc_response = self.eaa.create_object(self.app_handle, "CH01", "Chart", "qHyperCubeDef", hc_def)
        hc_handle = self.ega.get_handle(hc_response)
        self.egoa.get_layout(hc_handle)
        hc_data = self.egoa.get_hypercube_data(hc_handle, "/qHyperCubeDef", [nx_page])
        no_of_columns = len(list_of_dimensions)+len(list_of_measures)
        return hc_data, no_of_columns

    @staticmethod
    def convert_hypercube_to_matrix(hc_data, no_of_columns):
        rows = hc_data["qDataPages"][0]['qMatrix']
        matrix = [[0 for x in range(no_of_columns)] for y in range(len(rows))]
        for col_idx, row in enumerate(rows):
            for cell_idx, cell_val in enumerate(row):
                matrix[col_idx][cell_idx] = cell_val['qText']
        return [list(i) for i in zip(*matrix)]

    @staticmethod
    def convert_hypercube_to_inline_table(hc_data, table_name, no_of_columns):
        rows = hc_data["qDataPages"][0]['qMatrix']
        script = str.format('{0}:{1}Load * Inline[{1}',table_name, '\r\n')
        inline_rows = ''
        header_row = ''
        for col_idx in range(len(rows)):
            header_row = header_row + str.format('Column{0}{1}', col_idx, ',')
        header_row = header_row[:-1] + '\r\n'
        for row in rows:
            for cell_val in row:
                inline_rows = inline_rows + cell_val['qText'] + ','
            inline_rows = inline_rows[:-1] + '\r\n'
        return script + header_row + inline_rows + '];'

    def select_in_dimension(self,dimension_name, list_of_values):
        lb_field = self.eaa.get_field(self.app_handle, dimension_name)
        fld_handle = self.ega.get_handle(lb_field)
        values_to_select = []
        for val in list_of_values:
            val = {'qText': val}
            values_to_select.append(val)
        return self.efa.select_values(fld_handle, values_to_select)

    def delete_app(self, app_name):
        return self.ega.delete_app(app_name)['qSuccess']

    def disconnect(self):
        self.conn.close_qvengine_connection(self.conn)

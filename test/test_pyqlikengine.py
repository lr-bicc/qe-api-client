import unittest
from qe_api_client.engine import QixEngine


class TestQixEngine(unittest.TestCase):

    def setUp(self):
        self.qixe = QixEngine('ws://localhost:4848/app')
        self.app = self.qixe.ega.create_app("test_app")["qAppId"]
        opened_app = self.qixe.ega.open_doc(self.app)
        with open('./test_data/ctrl00_script.qvs') as f:
            script = f.read()
        self.app_handle = self.qixe.get_handle(opened_app)
        self.qixe.eaa.set_script(self.app_handle, script)
        self.assertTrue(self.qixe.eaa.do_reload_ex(self.app_handle)['qResult']['qSuccess'],'Failed to load script')

    def test_select_clear_in_dimension(self):
        select_result = self.qixe.select_in_field(self.app_handle, 'Alpha',['A', 'C', 'E'])
        self.assertTrue(select_result, "Failed to select values")
        self.assertTrue(self.qixe.clear_selection_in_dimension(self.app_handle, 'Alpha'),
                        'Failed to clear selection')

    def test_select_clear_all_in_dimension(self):
        select_result = self.qixe.select_in_field(self.app_handle, 'Alpha', ['A', 'C', 'E'])
        self.assertTrue(select_result, "Failed to select values")
        self.qixe.eaa.clear_all(self.app_handle)

    def test_select_excluded(self):
        self.qixe.select_in_field(self.app_handle, 'Alpha',['A', 'C', 'E'])
        select_result = self.qixe.select_excluded_in_field(self.app_handle, 'Alpha')
        self.assertTrue(select_result,'Failed to select excluded')

    def test_select_possible(self):
        select_result = self.qixe.select_possible_in_field(self.app_handle, 'Alpha')
        self.assertTrue(select_result,'Failed to select possible')

    def test_get_list_object_data(self):
        self.assertTrue(len(self.qixe.get_list_object_data(self.app_handle, 'Alpha')) == 2,
                        'Failed to get value list')

    def test_get_constructed_table_data(self):
        dim_1 = self.qixe.create_single_master_dimension(self.app_handle, dim_title="Dim 1", dim_def="Dim1", dim_label="'Dimension 1'")
        dim_2 = self.qixe.create_single_master_dimension(self.app_handle, dim_title="Dim 2", dim_def="Dim2", dim_label="'Dimension 2'")
        dim_1_id = dim_1["qGenericId"]
        dim_2_id = dim_2["qGenericId"]

        list_of_dimensions = ["Dim3"]
        list_of_master_dimensions = [dim_1_id, dim_2_id]
        list_of_measures = ["Sum(Expression3)"]
        list_of_master_measures = []
        # list_of_master_measures = ["snmpR", "1ad7060c-56ec-46d1-b83a-ff1393e0b236"]

        df = self.qixe.get_constructed_table_data(self.app_handle, list_of_dimensions, list_of_measures,
                                             list_of_master_dimensions, list_of_master_measures)
        print(df)

    def tearDown(self):
        self.assertTrue(self.qixe.ega.delete_app(self.app),'Failed to delete app')
        self.qixe.conn.close_qvengine_connection(self.qixe.conn)

if __name__ == '__main__':
    unittest.main()

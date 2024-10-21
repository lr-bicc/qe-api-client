import unittest
from qe_api_client.engine import QixEngine
from test.test_api import app_handle


class TestQixEngine(unittest.TestCase):

    def setUp(self):
        self.qixe = QixEngine('ws://localhost:4848/app')
        self.app = self.qixe.ega.create_app("test_app")["qAppId"]
        opened_app = self.qixe.ega.open_doc(self.app)
        with open('./test_data/ctrl00_script.qvs') as f:
            script = f.read()
        self.app_handle = self.qixe.get_handle(opened_app)
        self.qixe.eaa.set_script(app_handle, script)
        self.assertTrue(self.qixe.eaa.do_reload_ex(app_handle)['qResult']['qSuccess'],'Failed to load script')

    # def test_create_hypercube(self):
    #     hc = self.qixe.create_hypercube(1, ['Dim1', 'Dim2'],
    #                                     ['=Sum(Expression1)',
    #                                      '=Sum(Expression2)',
    #                                      '=Sum(Expression3)'])
    #     hc_cols = self.qixe.convert_hypercube_to_matrix(hc[0], hc[1])
    #     self.assertTrue(len(hc_cols) == 5,
    #                     'Failed to return proper number of columns')
    #     self.inline_table = self.qixe.convert_hypercube_to_inline_table(hc[0], 'MyTable')  # NOQA
    #     self.assertTrue(self.inline_table.startswith('MyTable'),
    #                     'Failed to create inline statement from hypercube')
    #     self.mtrx = self.qixe.convert_hypercube_to_matrix(hc[0], hc[1])
    #     self.assertTrue(len(self.mtrx) == 5,
    #                     'Failed to create matrix from hypercube')

    def test_select_clear_in_dimension(self):
        select_result = self.qixe.select_in_dimension(app_handle, 'Alpha',['A', 'C', 'E'])
        self.assertTrue(select_result["change"] == [1, 2],"Failed to select values")
        self.assertTrue(select_result["result"]['qReturn'],"Failed to select values")
        self.assertTrue(self.qixe.clear_selection_in_dimension(app_handle, 'Alpha'),
                        'Failed to clear selection')

    def test_select_clear_all_in_dimension(self):
        select_result = self.qixe.select_in_dimension(app_handle, 'Alpha', ['A', 'C', 'E'])
        self.assertTrue(select_result["change"] == [1, 2],"Failed to select values")
        self.assertTrue(select_result["result"]['qReturn'],"Failed to select values")
        self.qixe.eaa.clear_all(app_handle)

    def test_select_excluded(self):
        self.qixe.select_in_dimension(app_handle, 'Alpha',['A', 'C', 'E'])
        select_result = self.qixe.select_excluded_in_dimension(app_handle, 'Alpha')
        self.assertTrue(select_result,'Failed to select excluded')

    def test_select_possible(self):
        select_result = self.qixe.select_possible_in_dimension(app_handle, 'Alpha')
        self.assertTrue(select_result,'Failed to select possible')

    def test_get_list_object_data(self):
        self.assertTrue(len(self.qixe.get_list_object_data(app_handle, 'Alpha')) == 26,
                        'Failed to get value list')

    def tearDown(self):
        self.assertTrue(self.qixe.ega.delete_app(self.app),'Failed to delete app')

if __name__ == '__main__':
    unittest.main()

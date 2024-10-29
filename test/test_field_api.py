import unittest
from qe_api_client.engine import QixEngine


class TestFieldApi(unittest.TestCase):

    def setUp(self):
        url = 'ws://localhost:4848/app'
        self.qixe = QixEngine(url)
        self.app = self.qixe.ega.create_app("test_app")["qAppId"]
        opened_app = self.qixe.ega.open_doc(self.app)
        with open('./test_data/ctrl00_script.qvs') as f:
            script = f.read()
        self.app_handle = self.qixe.get_handle(opened_app)
        self.qixe.eaa.set_script(self.app_handle, script)
        self.qixe.eaa.do_reload_ex(self.app_handle)

        nx_inline_dimension_def = self.qixe.structs.nx_inline_dimension_def(["Alpha"])
        nx_page_initial = self.qixe.structs.nx_page(0, 0, 1, 26)
        lb_def = self.qixe.structs.list_object_def("$", "", nx_inline_dimension_def,[nx_page_initial])

        # Create info structure
        nx_info = self.qixe.structs.nx_info("ListObject", "SLB01")

        # Create generic object properties structure
        gen_obj_props = self.qixe.structs.generic_object_properties(nx_info, "qListObjectDef", lb_def)
        listobj = self.qixe.eaa.create_session_object(self.app_handle, gen_obj_props)  # NOQA

        self.lb_handle = self.qixe.get_handle(listobj)
        self.qixe.egoa.get_layout(self.lb_handle)
        self.lb_field = self.qixe.eaa.get_field(self.app_handle, "Alpha")
        self.fld_handle = self.qixe.get_handle(self.lb_field)

    def test_select_values(self):
        values_to_select = [{'qText': 'A'}, {'qText': 'B'}, {'qText': 'C'}]
        sel_res = self.qixe.efa.select_values(self.fld_handle, values_to_select)
        self.assertTrue(sel_res is True,"Failed to perform selection")
        val_mtrx = self.qixe.egoa.get_layout(self.lb_handle)["qListObject"]["qDataPages"][0]["qMatrix"]  # NOQA
        self.assertEqual(val_mtrx[0][0]["qState"],"S","Failed to select first value")
        self.assertEqual(val_mtrx[4][0]["qState"],"X","Failed to exclude fifth value")
        self.qixe.eaa.clear_all(self.app_handle)
        val_mtrx = self.qixe.egoa.get_layout(self.lb_handle)["qListObject"]["qDataPages"][0]["qMatrix"]  # NOQA
        self.assertEqual(val_mtrx[0][0]["qState"],"O","Failed to clear selection")
        self.assertEqual(val_mtrx[4][0]["qState"],"O","Failed to clear selection")

    def tearDown(self):
        self.qixe.ega.delete_app(self.app)
        self.qixe.conn.close_qvengine_connection(self.qixe.conn)


if __name__ == '__main__':
    unittest.main()

import unittest

from qe_api_client.api_classes.engine_app_api import EngineAppApi
from qe_api_client.engine_communicator import EngineCommunicator
from qe_api_client.api_classes.engine_field_api import EngineFieldApi
from qe_api_client.api_classes.engine_global_api import EngineGlobalApi
import qe_api_client.structs as structs

from qe_api_client.api_classes.engine_generic_object_api import EngineGenericObjectApi


class TestFieldApi(unittest.TestCase):

    def setUp(self):
        url = 'ws://localhost:4848/app'
        self.conn = EngineCommunicator(url)
        self.ega = EngineGlobalApi(self.conn)
        self.eaa = EngineAppApi(self.conn)
        self.egoa = EngineGenericObjectApi(self.conn)
        self.efa = EngineFieldApi(self.conn)
        self.struct = structs
        self.app = self.ega.create_app("TestApp")["qAppId"]
        opened_app = self.ega.open_doc(self.app)
        self.app_handle = self.ega.get_handle(opened_app)
        with open('../test/test_data/ctrl00_script.qvs') as f:
            script = f.read()
        self.eaa.set_script(self.app_handle, script)
        self.eaa.do_reload_ex(self.app_handle)
        nx_page_initial = structs.nx_page(0, 0, 1, 26)
        self.lb_def = structs.list_object_def("$", "",
                                              ["Alpha"],
                                              None,
                                              None,
                                              [nx_page_initial])
        self.lb_param = {"qInfo": {"qId": "SLB01", "qType": "ListObject"},
                         "qListObjectDef": self.lb_def}
        self.lb_sobject = self.eaa.create_session_object(self.app_handle,
                                                         self.lb_param)
        self.lb_handle = self.ega.get_handle(self.lb_sobject)
        self.egoa.get_layout(self.lb_handle)
        self.lb_field = self.eaa.get_field(self.app_handle, "Alpha")
        self.fld_handle = self.ega.get_handle(self.lb_field)

    def test_select_values(self):
        values_to_select = [{'qText': 'A'}, {'qText': 'B'}, {'qText': 'C'}]
        sel_res = self.efa.select_values(self.fld_handle, values_to_select)
        self.assertTrue(sel_res["qReturn"] is True,
                        "Failed to perform selection")
        val_mtrx = self.egoa.get_layout(self.lb_handle)["qListObject"]["qDataPages"][0]["qMatrix"]  # NOQA
        self.assertEqual(val_mtrx[0][0]["qState"],
                         "S",
                         "Failed to select first value")
        self.assertEqual(val_mtrx[4][0]["qState"],
                         "X",
                         "Failed to exclude fifth value")
        self.eaa.clear_all(self.app_handle)
        val_mtrx = self.egoa.get_layout(self.lb_handle)["qListObject"]["qDataPages"][0]["qMatrix"]  # NOQA
        self.assertEqual(val_mtrx[0][0]["qState"],
                         "O",
                         "Failed to clear selection")
        self.assertEqual(val_mtrx[4][0]["qState"],
                         "O",
                         "Failed to clear selection")

    def tearDown(self):
        self.ega.delete_app(self.app)
        self.conn.close_qvengine_connection(self.conn)


if __name__ == '__main__':
    unittest.main()

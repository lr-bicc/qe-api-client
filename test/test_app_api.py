import unittest
from qe_api_client.engine import QixEngine


class TestAppApi(unittest.TestCase):

    # Constructor to prepare everything before running the tests.
    def setUp(self):
        url = 'ws://localhost:4848/app'
        self.qixe = QixEngine(url)
        self.app = self.qixe.ega.create_app("TestApp")['qAppId']
        opened_app = self.qixe.ega.open_doc(self.app)
        self.app_handle = self.qixe.get_handle(opened_app)

    def test_add_alternate_state(self):
        response = self.qixe.eaa.add_alternate_state(self.app_handle, "MyState")
        self.assertEqual(response, {}, "Failed to add alternate state")

    def test_create_hypercube_object(self):
        with open('../test/test_data/ctrl00_script.qvs') as f:
            script = f.read()
        self.qixe.eaa.set_script(self.app_handle, script)
        self.qixe.eaa.do_reload_ex(self.app_handle)

        # Create the inline dimension structures
        hc_inline_dim1 = self.qixe.structs.nx_inline_dimension_def(["Dim1"])
        hc_inline_dim2 = self.qixe.structs.nx_inline_dimension_def(["Dim2"])

        # Create a sort structure
        hc_mes_sort = self.qixe.structs.sort_criteria()

        # Create the measure structures
        hc_inline_mes1 = self.qixe.structs.nx_inline_measure_def(definition="Sum(Expression1)")
        hc_inline_mes2 = self.qixe.structs.nx_inline_measure_def(definition="Sum(Expression2)")

        # Create hypercube dimensions from the inline dimension structures
        hc_dim1 = self.qixe.structs.nx_dimension("", hc_inline_dim1)
        hc_dim2 = self.qixe.structs.nx_dimension("", hc_inline_dim2)

        # Create hypercube measures from the inline measure structures
        hc_mes1 = self.qixe.structs.nx_measure("", hc_inline_mes1, hc_mes_sort)
        hc_mes2 = self.qixe.structs.nx_measure("", hc_inline_mes2, hc_mes_sort)

        # Create the paging model/structure (26 rows and 4 columns)
        nx_page = self.qixe.structs.nx_page(0, 0, 4, 26)

        # Create a hypercube definition with arrays of
        # hc dims, measures and nxpages
        hc_def = self.qixe.structs.hypercube_def("$",[hc_dim1, hc_dim2],[hc_mes1, hc_mes2])

        nx_info = self.qixe.structs.nx_info("table")
        gen_obj_props = self.qixe.structs.generic_object_properties(nx_info, "qHyperCubeDef", hc_def)

        # Create a Chart object with the hypercube definitions as parameter
        hc_response = self.qixe.eaa.create_session_object(self.app_handle, gen_obj_props)

        # Get the handle to the chart object (this may be different
        # in my local repo. I have made some changes to thisfor
        # future versions)
        hc_handle = self.qixe.get_handle(hc_response)

        # Validate the chart object by calling get_layout
        self.qixe.egoa.get_layout(hc_handle)

        # Call the get_hypercube_data to get the resulting json object,
        # using the handle and nx page as paramters
        hc_data = self.qixe.egoa.get_hypercube_data(hc_handle,"/qHyperCubeDef",nx_page)

        self.assertTrue(type(hc_data is {}),"Unexpected type of hypercube data")
        first_element_number = hc_data["qDataPages"][0]["qMatrix"][0][0]["qElemNumber"]  # NOQA
        first_element_text = hc_data["qDataPages"][0]["qMatrix"][0][0]["qText"]  # NOQA
        self.assertTrue(first_element_number == 0,"Incorrect value in first element number")
        self.assertTrue(first_element_text == "A","Incorrect value in first element text")

    def tearDown(self):
        self.qixe.ega.delete_app(self.app)
        self.qixe.conn.close_qvengine_connection(self.qixe.conn)


if __name__ == '__main__':
    unittest.main()

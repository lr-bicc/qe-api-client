import json


class EngineGenericObjectApi:
    """
    API class for interacting with Qlik Sense engine's generic objects, such as hypercubes, lists, and other
    data visualization objects.

    Methods:
        create_child(handle, params): Creates a generic object that is a child of another generic object.
        get_layout(handle): Retrieves the layout structure of a generic object.
        get_full_property_tree(handle): Retrieves the full property tree of a generic object.
        get_effective_properties(handle): Retrieves the effective properties of a generic object.
        get_hypercube_data(handle, path, pages): Retrieves the data from a hypercube.
        get_hypercube_pivot_data(handle, path, pages): Retrieves the pivot data from a hypercube.
        get_list_object_data(handle, path, pages): Retrieves the data from a list object.
    """

    def __init__(self, socket):
        """
        Initializes the EngineGenericObjectApi with a given socket connection.

        Parameters:
            socket (object): The socket connection to the Qlik Sense engine.
        """
        self.engine_socket = socket
    def create_child(self, handle, params):
        """
        Retrieves the layout structure of a specific generic object.

        Parameters:
            handle (int): The handle identifying the generic object.
            params (str): The parameters of the generic object.

        Returns:
            dict: The layout structure of the generic object (qLayout). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "CreateChild", "params": [params]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_layout(self, handle):
        """
        Retrieves the layout structure of a specific generic object.

        Parameters:
            handle (int): The handle identifying the generic object.

        Returns:
            dict: The layout structure of the generic object (qLayout). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetLayout", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qLayout"]
        except KeyError:
            return response["error"]

    def get_full_property_tree(self, handle):
        """
        Retrieves the full property tree of a specific generic object.

        Parameters:
            handle (int): The handle identifying the generic object.

        Returns:
            dict: The full property tree of the generic object (qPropEntry). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetFullPropertyTree", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]['qPropEntry']
        except KeyError:
            return response["error"]

    def get_effective_properties(self, handle):
        """
        Retrieves the effective properties of a specific generic object.

        Parameters:
            handle (int): The handle identifying the generic object.

        Returns:
            dict: The effective properties of the generic object (qProp). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetEffectiveProperties",
                          "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]['qProp']
        except KeyError:
            return response["error"]

    def get_hypercube_data(self, handle, path="/qHyperCubeDef", pages={}):
        """
        Retrieves the data from a specific hypercube in a generic object.

        Parameters:
            handle (int): The handle identifying the generic object containing the hypercube.
            path (str): The path to the hypercube definition within the object. Default is "/qHyperCubeDef".
            pages (list): A list of pages to retrieve from the hypercube data.

        Returns:
            dict: The data from the hypercube. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetHyperCubeData",
                          "params": {"qPath": path, "qPages": [pages]}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_hypercube_pivot_data(self, handle, path="/qHyperCubeDef", pages={}):
        """
        Retrieves the pivot data from a specific hypercube in a generic object.

        Parameters:
            handle (int): The handle identifying the generic object containing the hypercube.
            path (str): The path to the hypercube definition within the object. Default is "/qHyperCubeDef".
            pages (list): A list of pages to retrieve from the hypercube pivot data.

        Returns:
            dict: The pivot data from the hypercube. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetHyperCubePivotData",
                          "params": {"qPath": path, "qPages": [pages]}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_hypercube_stack_data(self, handle, path="/qHyperCubeDef", pages={}, max_no_cells=10000):
        """
        Retrieves the values of a stacked pivot table. It is possible to retrieve specific pages of data.

        Parameters:
            handle (int): The handle identifying the generic object containing the hypercube.
            path (str): The path to the hypercube definition within the object. Default is "/qHyperCubeDef".
            pages (list): A list of pages to retrieve from the hypercube pivot data.
            max_no_cells (int): Maximum number of cells at outer level. The default value is 10 000.


        Returns:
            dict: The pivot data from the hypercube. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetHyperCubeStackData",
                          "params": {"qPath": path, "qPages": [pages], "qMaxNbrCells": max_no_cells}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_list_object_data(self, handle, path="/qListObjectDef", pages=[]):
        """
        Retrieves the data from a specific list object in a generic object.

        Parameters:
            handle (int): The handle identifying the generic object containing the list object.
            path (str): The path to the list object definition within the object. Default is "/qListObjectDef".
            pages (list): A list of pages to retrieve from the list object data.

        Returns:
            dict: The data from the list object. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle,
                          "method": "GetListObjectData",
                          "params": [path, pages]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket,
                                                           msg)
                              )
        try:
            return response["result"]
        except KeyError:
            return response["error"]

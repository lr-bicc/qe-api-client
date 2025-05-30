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

    def apply_patches(self, handle: int, patches: list, soft_patch: bool = False):
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties. It is possible to
        apply a patch to the properties of a generic object, that is not persistent. Such a patch is called a soft patch.
        In that case, the result of the operation on the properties (add, remove or delete) is not shown when doing
        GetProperties, and only a GetLayout call shows the result of the operation. Properties that are not persistent
        are called soft properties. Once the engine session is over, soft properties are cleared. It should not be
        possible to patch "/qInfo/qId", and it will be forbidden in the near future.

        Parameters:
            handle (int): The handle identifying the generic object.
            patches (list): List of patches.
            soft_patch (bool, optional): If set to true, it means that the properties to be applied are not persistent.
            The patch is a soft patch. The default value is false.

        Returns:
            dict: Operation succeeded.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "ApplyPatches",
                          "params": {"qPatches": patches, "qSoftPatch": soft_patch}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def create_child(self, handle: int, prop: dict, prop_for_this: dict = None):
        """
        Creates a generic object that is a child of another generic object.

        Parameters:
            handle (int): The handle identifying the generic object.
            prop (dict): Information about the child. It is possible to create a child that is linked to another object.
            prop_for_this (dict, optional): Identifier of the parent's object. Should be set to update the properties of
            the parent's object at the same time the child is created.

        Returns:
            dict: The layout structure of the generic object (qLayout). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "CreateChild",
                          "params": {"qProp": prop, "qPropForThis": prop_for_this}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
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


    def get_properties(self, handle: int):
        """
        Retrieves the properties of a specific generic object.

        Parameters:
            handle (int): The handle identifying the generic object.

        Returns:
            dict: The properties of the generic object (qLayout). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetProperties", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qProp"]
        except KeyError:
            return response["error"]
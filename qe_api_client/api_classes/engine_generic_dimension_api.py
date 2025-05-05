import json


class EngineGenericDimensionApi:
    """
    API class for interacting with Qlik Sense engine's generic dimension objects.

    Methods:
        get_dimension(handle, dimension_id): Retrieves the definition of a specific dimension.
    """

    def __init__(self, socket):
        """
        Initializes the EngineGenericDimensionApi with a given socket connection.

        Parameters:
            socket (object): The socket connection to the Qlik Sense engine.
        """
        self.engine_socket = socket

    def get_dimension(self, app_handle: int, dimension_id: str):
        """
        Retrieves the definition of a specific dimension from the Qlik Sense engine.

        Parameters:
            app_handle (int): The handle identifying the application.
            dimension_id (str): The unique identifier (qId) of the dimension to retrieve.

        Returns:
            dict: The definition of the requested dimension (qReturn). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": app_handle, "method": "GetDimension",
                          "params": {"qId": dimension_id}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

    def apply_patches(self, handle: int, patches: list):
        """
        Applies a patch to the properties of an object. Allows an update to some of the properties.

        Parameters:
            handle (int): The handle identifying the generic object.
            patches (list): List of patches.

        Returns:
            dict: Operation succeeded.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "ApplyPatches",
                          "params": {"qPatches": patches}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]
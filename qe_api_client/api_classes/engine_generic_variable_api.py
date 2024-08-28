import json


class EngineGenericVariableApi:
    """
    API class for interacting with Qlik Sense engine's generic variable object.

    Methods:
        set_string_value(handle, str_val): Sets the value of a string variable.
        get_properties(handle): Retrieves the properties of a generic variable.
    """

    def __init__(self, socket):
        """
        Initializes the EngineGenericVariableApi with a given socket connection.

        Parameters:
            socket (object): The socket connection to the Qlik Sense engine.
        """
        self.engine_socket = socket

    def set_string_value(self, handle, str_val):
        """
        Sets the value of a string variable in the Qlik Sense engine.

        Parameters:
            handle (int): The handle identifying the variable.
            str_val (str): The string value to set for the variable.

        Returns:
            dict: The result of the set operation. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "SetStringValue",
                          "params": {"qVal": str_val}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_properties(self, handle):
        """
        Retrieves the properties of a generic variable from the Qlik Sense engine.

        Parameters:
            handle (int): The handle identifying the variable.

        Returns:
            dict: The properties of the generic variable. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetProperties", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]
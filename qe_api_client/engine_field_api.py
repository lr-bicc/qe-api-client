import json


class EngineFieldApi:
    """
    A client for interacting with the Qlik Engine JSON API for field operations.

    Args:
        socket: An object representing the engine socket connection used to communicate with the Qlik Engine.
    """

    def __init__(self, socket):
        """
        Initializes the EngineFieldApi with the provided socket.

        Args:
            socket: An engine socket object used to send and receive messages from the Qlik Engine.
        """
        self.engine_socket = socket

    def select(self, fld_handle, value):
        """
        Selects a specific value in a field.

        Args:
            fld_handle (int): The handle of the field.
            value (str): The value to select.

        Returns:
            dict: The response from the engine, containing the result or an error message.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "Select",
                          "params": [value, False, 0]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response
        except KeyError:
            return response["error"]

    def select_values(self, fld_handle, values=None):
        """
        Selects multiple values in a field.

        Args:
            fld_handle (int): The handle of the field.
            values (list, optional): A list of values to select. Defaults to an empty list.

        Returns:
            dict: The response from the engine, containing the result or an error message.
        """
        if values is None:
            values = []
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectValues",
                          "params": [values, False, False]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response
        except KeyError:
            return response["error"]

    def select_excluded(self, fld_handle):
        """
        Selects all excluded values in a field.

        Args:
            fld_handle (int): The handle of the field.

        Returns:
            dict: The response from the engine, containing the result or an error message.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectExcluded", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def select_possible(self, fld_handle):
        """
        Selects all possible values in a field.

        Args:
            fld_handle (int): The handle of the field.

        Returns:
            dict: The response from the engine, containing the result or an error message.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectPossible", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def clear(self, fld_handle):
        """
        Clears the selection in a field.

        Args:
            fld_handle (int): The handle of the field.

        Returns:
            dict: The response from the engine, containing the result or an error message.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "Clear", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_cardinal(self, fld_handle):
        """
        Gets the number of distinct values in a field.

        Args:
            fld_handle (int): The handle of the field.

        Returns:
            int: The number of distinct values in the field, or an error message.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "GetCardinal", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

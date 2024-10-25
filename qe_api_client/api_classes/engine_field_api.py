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

    def select(self, fld_handle, value, soft_lock = False, excluded_values_mode = 0):
        """
        Selects field values matching a search string.

        Args:
            fld_handle (int): The handle of the field.
            value (str): String to search for. Can contain wild cards or numeric search criteria.
            soft_lock (bool): Set to true to ignore locks; in that case, locked fields can be selected.
            excluded_values_mode (int): Include excluded values in search.

        Returns:
            dict: The response from the engine, containing the result or an error message.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "Select",
                          "params": {"qMatch": value, "qSoftLock": soft_lock,
                                     "qExcludedValuesMode": excluded_values_mode}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response
        except KeyError:
            return response["error"]

    def select_values(self, fld_handle, values, toggle_mode = False, soft_lock = False):
        """
        Selects multiple values in a field.

        Args:
            fld_handle (int): The handle of the field.
            values (list): A list of field values to select. Mandatory field.
            toggle_mode (bool): The default value is false.
            soft_lock (bool): Set to true to ignore locks; in that case, locked fields can be selected.
            The default value is false.

        Returns:
            dict: The response from the engine, containing the result or an error message.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectValues",
                          "params": {"qFieldValues": values, "qToggleMode": toggle_mode, "qSoftLock": soft_lock}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

    def select_excluded(self, fld_handle, soft_lock=False):
        """
        Inverts the current selections.

        Args:
            fld_handle (int): The handle of the field.
            soft_lock (bool): Set to true to ignore locks; in that case, locked fields can be selected.
            The default value is false.

        Returns:
            bool: true/false. The operation is successful if qReturn is set to true.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectExcluded",
                          "params": {"qSoftLock": soft_lock}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

    def select_possible(self, fld_handle, soft_lock=False):
        """
        Selects all possible values in a field.

        Args:
            fld_handle (int): The handle of the field.
            soft_lock (bool): Set to true to ignore locks; in that case, locked fields can be selected.
            The default value is false.

        Returns:
            bool: true/false. The operation is successful if qReturn is set to true.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "SelectPossible",
                          "params": {"qSoftLock": soft_lock}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
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
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "Clear", "params": {}})
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
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": fld_handle, "method": "GetCardinal", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

import json


class EngineGenericMeasureApi:
    """
    API class for interacting with Qlik Sense engine's generic measure objects.

    Methods:
        get_measure(handle, measure_id): Retrieves the definition of a specific measure.
    """

    def __init__(self, socket):
        """
        Initializes the EngineGenericMeasureApi with a given socket connection.

        Parameters:
            socket (object): The socket connection to the Qlik Sense engine.
        """
        self.engine_socket = socket

    def get_measure(self, handle, measure_id):
        """
        Retrieves the definition of a specific measure from the Qlik Sense engine.

        Parameters:
            handle (int): The handle identifying the measure object.
            measure_id (str): The unique identifier (qId) of the measure to retrieve.

        Returns:
            dict: The definition of the requested measure (qReturn). In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetMeasure", "params": {"qId": measure_id}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

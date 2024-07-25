import json


class EngineGenericDimensionApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def get_dimension(self, handle, dimension_id):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetDimension",
                          "params": {"qId": dimension_id}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

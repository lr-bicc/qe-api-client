import json


class EngineGenericVariableApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def set_string_value(self, handle, str_val):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "SetStringValue",
                          "params": {"qVal": str_val}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_properties(self, handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetProperties", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]
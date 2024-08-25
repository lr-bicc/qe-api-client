import json


class EngineGenericMeasureApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def get_measure(self, handle, measure_id):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetMeasure", "params": {"qId": measure_id}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

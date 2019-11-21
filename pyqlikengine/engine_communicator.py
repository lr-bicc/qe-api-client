from websocket import create_connection
import ssl


class EngineCommunicator:

    def __init__(self, url):
        self.url = url
        self.ws = create_connection(self.url)
        # Holds session object. Required for Qlik Sense Sept. 2017 and later
        self.session = self.ws.recv()

    @staticmethod
    def send_call(self, call_msg):
        self.ws.send(call_msg)
        return self.ws.recv()

    @staticmethod
    def close_qvengine_connection(self):
        self.ws.close()


class SecureEngineCommunicator(EngineCommunicator):

    def __init__(self, url, user_directory,
                 user_id, ca_certs, certfile,
                 keyfile, app_id=None
                 ):
        self.url = "wss://" + url + ":4747/app/" + str(app_id)
        certs = ({"ca_certs": ca_certs,
                  "certfile": certfile,
                  "keyfile": keyfile,
                  "cert_reqs": ssl.CERT_NONE,
                  "server_side": False
                  })

        ssl.match_hostname = lambda cert, hostname: True
        header = f'X-Qlik-User: UserDirectory={user_directory}; UserId={user_id}'  # NOQA
        self.ws = create_connection(
                self.url, sslopt=certs,
                cookie=None, header={header})
        self.session = self.ws.recv()

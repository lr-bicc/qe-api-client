# Qlik Engine API Client

Python client for the [Qlik Engine JSON API](https://help.qlik.com/en-US/sense-developer/November2024/Subsystems/EngineAPI/Content/Sense_EngineAPI/introducing-engine-API.htm)

Forked from [jhettler/pyqlikengine](https://github.com/jhettler/pyqlikengine)

## Requirements
* Python 3.6+
* websocket-client>=0.47.0

## Installation
```bash
pip install qe-api-client
```

## Connecting to Qlik Sense Enterprise Server
You need to export the Qlik Sense certificates in PEM format from the Qlik Sense Enterprise server to a local folder in 
order to authenticate on the server.

```python
from qe_api_client.engine import QixEngine

url = 'qlik-1.ad.xxx.xxx'
user_directory = 'UserDomainToQlikLogin'
user_id = 'sense'
ca_certs = 'qlik_certs/qlik-1_root.pem'
certfile = 'qlik_certs/qlik-1_client.pem'
keyfile = 'qlik_certs/qlik-1_client_key.pem'
qixe = QixEngine(url=url, user_directory=user_directory, user_id=user_id, ca_certs=ca_certs, certfile=certfile, 
                 keyfile=keyfile)

# print all apps in Qlik Server
print(qixe.ega.get_doc_list())
```

## Connecting to Qlik Sense Desktop
You need to start your Qlik Sense Desktop client on your local PC.

```python
from qe_api_client.engine import QixEngine

url = 'ws://localhost:4848/app'
qixe = QixEngine(url=url)

# print all apps in Qlik Server
print(qixe.ega.get_doc_list())
```

## Examples of usage
Please click on this [link](https://github.com/lr-bicc/qe-api-client/tree/master/examples) to find examples of usage of this client.

## API reference
Please click on this [link](https://lr-bicc.github.io/qe-api-client) for full API reference documentation .
# Qlik Engine API Client

Python wrapper around [Qlik Engine JSON API](https://help.qlik.com/en-US/sense-developer/February2024/Subsystems/EngineAPI/Content/Sense_EngineAPI/introducing-engine-API.htm)

Forked from [jhettler/pyqlikengine](https://github.com/jhettler/pyqlikengine)

## Requirements
* Python 3.6+
* websocket-client>=0.47.0

## Getting started instructions
1. Install client
```bash
pip install qe-api-client
```
2. Export the qlik sense certificates in PEM format to a local folder.
3. Launch Python
4. Import the Qlik Engine API Client in your Python script.

## Example of usage
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

## API reference
Please click on this [link](https://lr-bicc.github.io/qe-api-client) for full API reference documentation .
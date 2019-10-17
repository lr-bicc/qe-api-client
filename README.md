# pyqlikengine

Python wrapper around [Qlik Engine JSON API](https://help.qlik.com/en-US/sense-developer/June2019/Subsystems/EngineAPI/Content/Sense_EngineAPI/introducing-engine-API.htm)

Forked from [qliknln/pyqlikengine](https://github.com/qliknln/pyqlikengine)

## Requirements
* Python 3.6+
* websocket-client>=0.47.0

## Example of usage
```bash
pip install pyqlikengine
```
```python
from pyqlikengine.engine import QixEngine

url = 'qlik-1.ad.xxx.xxx'
user_directory = 'UserDomainToQlikLogin'
user_id = 'sense'
ca_certs = 'qlik_certs/qlik-1_root.pem'
certfile = 'qlik_certs/qlik-1_client.pem'
keyfile = 'qlik_certs/qlik-1_client_key.pem'
qixe = QixEngine(url=url, user_directory=user_directory,
                 user_id=user_id, ca_certs=ca_certs,
                 certfile=certfile, keyfile=keyfile)

# print all apps in Qlik Server
print(qixe.ega.get_doc_list())
```

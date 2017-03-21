python-estimote
===============
Python wrapper for Estimote API

Installation
------------
```
pip install -e https://github.com/michal-michalak/python-estimote
```

Requires
--------
    * requests
 
 
Usage
-----

```python
from pyestimote.client import EstimoteAPI
client = EstimoteAPI(app_id='YOUR_APP_ID', app_token='YOUR_APP_TOKEN')
response = client.get_devices()
devices = response.json()
```
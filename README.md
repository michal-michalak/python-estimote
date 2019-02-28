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

devices = client.get_device(identifier='c119c2c5e236').json()
devices = client.get_devices(page=3).json()

devices = client.search(page=2, q='mint')
devices = client.search_all(q='mint')

devices = client.get_devices_by_identifiers(identifiers=['c119c2c5e236', 'cb5h32be1fe7']).json()
```
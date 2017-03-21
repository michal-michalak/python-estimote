from __future__ import unicode_literals

import requests

from .exceptions import (
    EstimoteAPIBadRequest, EstimoteAPIUnauthorized, EstimoteAPIForbidden, EstimoteAPINotFound,
    EstimoteInternalServerError
)


class EstimoteAPI(object):
    def __init__(self, app_id, app_token):
        self.app_id = app_id
        self.app_token = app_token
        self.host = 'cloud.estimote.com'
        self.base_path = '/v2'
        self.base_url = 'https://' + self.host + self.base_path
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method, url, **kwargs):
        kwargs.update({'auth': (self.app_id, self.app_token)})
        kwargs.update({'headers': self.headers})
        response = requests.request(method, url, **kwargs)

        if response.status_code == 400:
            raise EstimoteAPIBadRequest(response=response)
        elif response.status_code == 401:
            raise EstimoteAPIUnauthorized(response=response)
        elif response.status_code == 403:
            raise EstimoteAPIForbidden(response=response)
        elif response.status_code == 404:
            raise EstimoteAPINotFound(response=response)
        elif response.status_code == 500:
            raise EstimoteInternalServerError(response=response)

        return response

    def delete_pending_settings(self, identifiers=None):
        """ https://cloud.estimote.com/docs/#api-Devices-DeletePendingSettings """
        url = self.base_url + '/devices/delete_pending_settings/'
        identifiers = identifiers or []
        data = {"identifiers": identifiers}
        return self._make_request('POST', url, data=data)

    def get_devices(self):
        """ https://cloud.estimote.com/docs/#api-Devices-GetDevices """
        url = self.base_url + '/devices/'
        return self._make_request('GET', url)

    def get_device(self, identifier):
        """ https://cloud.estimote.com/docs/#api-Devices-GetDevice """
        url = self.base_url + '/devices/{}/'.format(identifier)
        return self._make_request('GET', url)

    def get_devices_to_be_updated(self):
        """ https://cloud.estimote.com/docs/#api-Devices-GetDevicesPending """
        url = self.base_url + '/devices/pending/'
        return self._make_request('GET', url)

    def get_newest_firmwares(self):
        """ https://cloud.estimote.com/docs/#api-DevicesV3-NewestFirmwares """
        url = 'https://' + self.host + '/v3/devices/newest_firmwares/'
        return self._make_request('GET', url)

    def update_device(self, identifier, data):
        """ https://cloud.estimote.com/docs/#api-Devices-UpdateDevice """
        url = self.base_url + '/devices/{}/'.format(identifier)
        return self._make_request('POST', url, data=data)

    def update_multiple_devices(self, data):
        """ https://cloud.estimote.com/docs/#api-Devices-UpdateDevices """
        url = self.base_url + '/devices/bulk/'
        return self._make_request('POST', url, data=data)

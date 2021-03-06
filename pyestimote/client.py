from __future__ import unicode_literals

import math
import urllib
import requests

from .exceptions import *


class EstimoteAPI(object):
    def __init__(self, app_id, app_token):
        self.app_id = app_id
        self.app_token = app_token
        self.host = 'cloud.estimote.com'
        self.base_v2_url = 'https://' + self.host + '/v2'
        self.base_v3_url = 'https://' + self.host + '/v3'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.page_size = 100 # according to documentation page size = 100

    def _make_request(self, method, url, **kwargs):
        kwargs.update({'auth': (self.app_id, self.app_token)})
        kwargs.update({'headers': self.headers})
        response = requests.request(method, url, **kwargs)

        if response.status_code == 400:
            raise EstimoteAPIBadRequest(response=response)
        elif response.status_code == 401:
            raise EstimoteAPIUnauthorized(response=response)
        elif response.status_code == 402:
            raise EstimoteAPIPaymentRequired(response=response)
        elif response.status_code == 403:
            raise EstimoteAPIForbidden(response=response)
        elif response.status_code == 404:
            raise EstimoteAPINotFound(response=response)
        elif response.status_code == 500:
            raise EstimoteInternalServerError(response=response)
        elif response.status_code == 503:
            raise EstimoteServiceUnavailable(response=response)

        return response

    def _get_total_pages(self, total_count):
        return int(math.ceil(total_count / float(self.page_size)))

    #####################################################################################
    # DEVICES
    #####################################################################################
    def get_device(self, identifier):
        """ https://cloud.estimote.com/docs/#api-Devices-GetDevice """
        url = self.base_v3_url + '/devices/{}/'.format(identifier)
        return self._make_request('GET', url)

    def get_devices(self,  **params):
        """ https://cloud.estimote.com/docs/#api-Devices-GetDevices """
        params['page'] = params.get('page', 1)
        url = self.base_v3_url + '/devices/?{}'.format(urllib.urlencode(params))
        return self._make_request('GET', url)

    def get_devices_by_identifiers(self, identifiers):
        """ https://cloud.estimote.com/docs/#api-Devices-GetDevices """
        assert bool(len(identifiers)), 'Pass not empty identifiers list.'
        params = urllib.urlencode({'identifiers': ','.join(identifiers)})
        url = self.base_v3_url + '/devices/?{}'.format(params)
        return self._make_request('GET', url)

    # TODO: update to v3 when official documentation will be updated
    def get_devices_to_be_updated(self):
        """ https://cloud.estimote.com/docs/#api-Devices-GetDevicesPending """
        url = self.base_v2_url + '/devices/pending/'
        return self._make_request('GET', url)

    # TODO: not supported anymore by Estimote? for v2 and v3 returns 400 all the time
    # def delete_pending_settings(self, identifiers=None):
    #     """ https://cloud.estimote.com/docs/#api-Devices-DeletePendingSettings """
    #     url = self.base_v2_url + '/devices/delete_pending_settings/'
    #     identifiers = identifiers or []
    #     data = {"identifiers": identifiers}
    #     return self._make_request('POST', url, data=data)

    def update_device(self, identifier, data):
        """ https://cloud.estimote.com/docs/#api-Devices-UpdateDevice """
        url = self.base_v3_url + '/devices/{}/'.format(identifier)
        data['identifier'] = identifier
        return self._make_request('POST', url, json=data)

    # TODO: update to v3 when official documentation will be updated
    def update_multiple_devices(self, data):
        """ https://cloud.estimote.com/docs/#api-Devices-UpdateDevices """
        url = self.base_v2_url + '/devices/bulk/'
        return self._make_request('POST', url, json=data)

    def get_newest_firmwares(self):
        """ https://cloud.estimote.com/docs/#api-DevicesV3-NewestFirmwares """
        url = self.base_v3_url + '/devices/newest_firmwares/'
        return self._make_request('GET', url)

    def search(self,  **params):
        """ Undocumented API endpoint - check web version of cloud.estimote.com """
        params['page'] = params.get('page', 1)
        url = self.base_v3_url + '/devices/search/?{}'.format(urllib.urlencode(params))
        return self._make_request('GET', url)

    def search_all(self, **params):
        """ Returns all devices (e.g. list of 321 items) matching *mint* phrase. Pagination is handled internally. """
        params.pop('page', None)
        json_data = self.search(**params).json()
        total_count = json_data['meta']['total_count']
        data = json_data['data']

        if total_count <= self.page_size:
            return data

        for page in range(2, self._get_total_pages(total_count) + 1):
            params['page'] = page
            page_data = self.search(**params).json()['data']
            data.extend(page_data)

        return data

    #####################################################################################
    # ATTACHMENTS
    #####################################################################################

    def create_attachment(self, identifier, attachment):
        """ https://cloud.estimote.com/docs/#api-Attachments-CreateAttachment """
        data = {'data': {'payload': attachment, 'identifier': identifier, 'for': 'device'}}
        url = self.base_v3_url + '/attachments/'
        return self._make_request('POST', url, json=data)

    def delete_attachment(self, id_):
        """ https://cloud.estimote.com/docs/#api-Attachments-DeleteAttachment """
        url = self.base_v3_url + '/attachments/{}'.format(id_)
        return self._make_request('DELETE', url)

    def get_attachment(self, id_):
        """ https://cloud.estimote.com/docs/#api-Attachments-GetAttachment """
        url = self.base_v3_url + '/attachments/{}'.format(id_)
        return self._make_request('GET', url)

    def get_attachments(self, page=None):
        """ https://cloud.estimote.com/docs/#api-Attachments-GetAttachments """
        page = page or 1
        params = urllib.urlencode({'page': page, 'for': 'device'})
        url = self.base_v3_url + '/attachments/?{}'.format(params)
        return self._make_request('GET', url)

    def get_device_attachment(self, identifier):
        """ https://cloud.estimote.com/docs/#api-Attachments-getDeviceAttachment """
        url = self.base_v3_url + '/devices/{}/attachment'.format(identifier)
        return self._make_request('GET', url)

    def update_attachment(self, id_, attachment):
        """ https://cloud.estimote.com/docs/#api-Attachments-UpdateAttachmentPayload """
        data = {'data': {'payload': attachment}}
        url = self.base_v3_url + '/attachments/{}'.format(id_)
        return self._make_request('PATCH', url, json=data)

    #####################################################################################
    # TAGS
    #####################################################################################

    def get_tags(self):
        """ https://cloud.estimote.com/docs/#api-Tags-Get_tags_list """
        url = self.base_v3_url + '/tags/'
        return self._make_request('GET', url)

    def get_identifiers_by_tag(self, tag):
        """ https://cloud.estimote.com/docs/#api-Tags-GetIdentifiersByTag """
        params = urllib.urlencode({'name': tag})
        url = self.base_v3_url + '/tags/devices?{}'.format(params)
        return self._make_request('GET', url)

    def update_device_tags(self, identifier, tags):
        """ https://cloud.estimote.com/docs/#api-Devices-UpdateDevice """
        """ https://cloud.estimote.com/docs/#api-Tags """
        data = {'shadow': {'tags': list(set(tags))}}
        return self.update_device(identifier, data=data)

    def update_multiple_devices_tags(self, identifiers, tags_matrix):
        """ https://cloud.estimote.com/docs/#api-Devices-UpdateDevices """
        """ https://cloud.estimote.com/docs/#api-Tags """
        assert len(identifiers) == len(tags_matrix), \
            'Collections of identifiers and tags_matrix should have same length'

        zipped = zip(identifiers, tags_matrix)
        data = [{
            'identifier': identifier,
            'shadow': {'tags': list(set(tags))}
        } for identifier, tags in zipped]
        return self.update_multiple_devices(data)

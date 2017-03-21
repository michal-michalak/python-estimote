from __future__ import unicode_literals

from requests import RequestException


class EstimoteAPIException(RequestException):
    pass


class EstimoteAPIBadRequest(EstimoteAPIException):
    pass


class EstimoteAPIUnauthorized(EstimoteAPIException):
    pass


class EstimoteAPIForbidden(EstimoteAPIException):
    pass


class EstimoteAPINotFound(EstimoteAPIException):
    pass


class EstimoteInternalServerError(EstimoteAPIException):
    pass

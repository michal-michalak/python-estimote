from __future__ import unicode_literals

from requests import RequestException

__all__ = [
    'EstimoteAPIException', 'EstimoteAPIBadRequest', 'EstimoteAPIUnauthorized', 'EstimoteAPIPaymentRequired',
    'EstimoteAPIForbidden', 'EstimoteAPINotFound', 'EstimoteInternalServerError', 'EstimoteServiceUnavailable'
]


class EstimoteAPIException(RequestException):
    pass


class EstimoteAPIBadRequest(EstimoteAPIException):
    pass


class EstimoteAPIUnauthorized(EstimoteAPIException):
    pass


class EstimoteAPIPaymentRequired(EstimoteAPIException):
    pass


class EstimoteAPIForbidden(EstimoteAPIException):
    pass


class EstimoteAPINotFound(EstimoteAPIException):
    pass


class EstimoteInternalServerError(EstimoteAPIException):
    pass


class EstimoteServiceUnavailable(EstimoteAPIException):
    pass

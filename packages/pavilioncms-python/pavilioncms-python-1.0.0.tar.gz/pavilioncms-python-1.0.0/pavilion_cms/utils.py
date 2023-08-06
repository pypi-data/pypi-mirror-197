import requests

from pavilion_cms.exceptions import (
    UserAuthError,
    UserNotAuthorized,
    BadRequest,
    ResourceNotFound,
)


def handle_errors(response):
    if response.status_code == requests.codes.unauthorized:
        raise UserAuthError()
    if response.status_code == requests.codes.bad_request:
        raise BadRequest()
    if response.status_code == requests.codes.not_found:
        raise ResourceNotFound()
    if response.status_code == requests.codes.forbidden:
        raise UserNotAuthorized()

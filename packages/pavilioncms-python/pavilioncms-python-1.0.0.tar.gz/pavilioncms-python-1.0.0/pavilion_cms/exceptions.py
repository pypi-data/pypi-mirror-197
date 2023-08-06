class BaseException(Exception):
    message = "An error occurred"

    def __init__(self, message=None, errors=None):
        if message is not None:
            self.message = message
        self.errors = errors
        super().__init__(self.message)


class UserAuthError(BaseException):
    """An error occurred while authenticating a user."""

    message = "Unable to Authenticate your account. Please check your Read Token"


class UserNotAuthorized(BaseException):
    """The user is not authorized to access this resource."""

    message = "You are not authorized to access this resource."


class ResourceNotFound(BaseException):
    """The resource was not found."""

    message = "The resource was not found."


class BadRequest(BaseException):
    """The request was not valid."""

    message = "The request was not valid."

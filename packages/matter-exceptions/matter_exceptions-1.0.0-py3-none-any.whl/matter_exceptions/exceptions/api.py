from matter_exceptions.base_api_exception import BaseAPIException


class ValidationError(BaseAPIException):
    STATUS_CODE = 400


class AccessDeniedError(BaseAPIException):
    STATUS_CODE = 403


class NotFoundError(BaseAPIException):
    STATUS_CODE = 404


class ConflictError(BaseAPIException):
    STATUS_CODE = 409


class UnprocessableError(BaseAPIException):
    STATUS_CODE = 422


class ServerError(BaseAPIException):
    STATUS_CODE = 500


class UnauthorizedError(BaseAPIException):
    STATUS_CODE = 401

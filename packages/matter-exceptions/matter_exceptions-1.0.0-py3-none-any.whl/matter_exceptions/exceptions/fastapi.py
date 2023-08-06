from matter_exceptions.base_fastapi_exception import BaseFastAPIException


class ValidationError(BaseFastAPIException):
    STATUS_CODE = 400


class AccessDeniedError(BaseFastAPIException):
    STATUS_CODE = 403


class NotFoundError(BaseFastAPIException):
    STATUS_CODE = 404


class ConflictError(BaseFastAPIException):
    STATUS_CODE = 409


class UnprocessableError(BaseFastAPIException):
    STATUS_CODE = 422


class ServerError(BaseFastAPIException):
    STATUS_CODE = 500


class UnauthorizedError(BaseFastAPIException):
    STATUS_CODE = 401

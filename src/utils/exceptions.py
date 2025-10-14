class AppException(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.detail = message
        self.status_code = status_code

class BadRequestException(AppException):
    def __init__(self, message = 'invalid_param') -> None:
        super().__init__(400, message)

class UnauthorizedException(AppException):
    def __init__(self, message='unauthorized'):
        super().__init__(401, message)

class ForbiddenException(AppException):
    def __init__(self, message='forbidden'):
        super().__init__(403, message)

class NotFoundException(AppException):
    def __init__(self, message = 'not_found') -> None:
        super().__init__(404, message)
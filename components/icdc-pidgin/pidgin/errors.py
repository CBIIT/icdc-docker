class PidginException(Exception):
    def __init__(self, message):
        self.message = str(message)
        self.code = 500


class AuthenticationException(PidginException):
    def __init__(self, message):
        self.message = str(message)
        self.code = 401


class ObjectNotFoundException(PidginException):
    def __init__(self, message):
        self.message = str(message)
        self.code = 404


class NoCoreMetadataException(PidginException):
    def __init__(self, message):
        self.message = str(message)
        self.code = 404

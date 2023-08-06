from django.core.exceptions import ValidationError

class KubefacetsException(ValidationError):
    def __init__(self, msg, error_code, status_code):
        self.__msg = msg
        self.__errorCode = error_code
        self.__statusCode = status_code

    def getMsg(self):
        return self.__msg

    def getErrorCode(self):
        return self.__errorCode

    def getStatusCode(self):
        return self.__statusCode
class ValidatonErrors:
    INVALID_JSON_DETAIL = "Invalid JSON format for detail"
    INVALID_JSON_CREDENTIAL = "Invalid JSON format for credential"

class ResponseErrors:
    BAD_REQUEST = "Something bad happend. Try again!"
    Permission_DENIED = "Permision denied"
    NOT_FOUND = "Not found!"


class Error(str):
    def __new__(cls, message:str):
        return message

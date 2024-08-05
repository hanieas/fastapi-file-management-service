class Errors:
    BAD_REQUEST: str = "Something bad happend. Try again!"
    Permission_DENIED: str = "Permision denied"
    NOT_FOUND: str = "Not found!"

class ValidatonErrors:
    INVALID_JSON_DETAIL: str = "Invalid JSON format for detail"
    INVALID_JSON_CREDENTIAL: str = "Invalid JSON format for credential"

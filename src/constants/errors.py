class Errors:
    BAD_REQUEST: str = "Something bad happend. Try again!"
    Permission_DENIED: str = "Permision denied"
    NOT_FOUND: str = "Not found!"
    FILE_NOT_FOUND: str = "File directory not found. Please initialize first!"

class ValidatonErrors:
    INVALID_JSON_DETAIL: str = "Invalid JSON format for detail"
    INVALID_JSON_CREDENTIAL: str = "Invalid JSON format for credential"
    LE_CHUNCK_SIZE: str = "File sile is larger than valid chunk size"

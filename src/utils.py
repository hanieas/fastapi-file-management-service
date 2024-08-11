import json
from fastapi.exceptions import RequestValidationError
from constants.errors import ValidatonErrors
from typing import Dict


def parse_json_to_dict(json_string: str, body: str) -> Dict[str, str]:
    parsed_dict = json.loads(json_string)

    if not isinstance(parsed_dict, dict):
        raise RequestValidationError(errors=[{
            'loc': ('body', body),
            'msg': ValidatonErrors.INVALID_JSON_CREDENTIAL,
            'type': 'value_error'
        }],
            body={body: "invalid_format"})
    return {str(key): str(value) for key, value in parsed_dict.items()}

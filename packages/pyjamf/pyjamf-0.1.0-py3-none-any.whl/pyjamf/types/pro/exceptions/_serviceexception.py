from typing import Dict, Any, List

from pyjamf.types.pro.exceptions._error import Error

class ServiceException(Exception):
    
    def __init__(self, status_code: int, errors: List[Error]) -> None:
        super().__init__(errors)
        
        self._status_code = status_code
        self._errors = errors
        
    @classmethod
    def from_json(cls, json: Dict[str, Any]):
        
        _status_code = json.get("httpStatus")
        _raw_errors = json.get("errors", [])
        
        _errors = []
        
        if len(_raw_errors) > 0:
            for error in _raw_errors:
                _errors.append(Error.from_json(error))
                
        return cls(_status_code, _errors)
    
    def __str__(self) -> str:
        
        return str([f"code: {error._code}, description: {error._description}, id: {error._id}" for error in self._errors])
import os

from typing import Dict, Any

class Error:
    
    def __init__(self, code, description, id, field):
        self._code = code
        self._description = description
        self._id = id
        self._field = field
    
    def __str__(self) -> str:
        error_string_builder = ""
        
        if self._code != None:
            error_string_builder += f"Code: {self._code}"
            error_string_builder += os.linesep
        
        if self._description != None:
            error_string_builder += f"Description: {self._description}"
            error_string_builder += os.linesep
        
        if self._id != None:
            error_string_builder += f"Id: {self._id}"
            error_string_builder += os.linesep
            
        if self._field != None:
            error_string_builder += f"Field: {self._field}"
            error_string_builder += os.linesep
            
        return error_string_builder
    
    @classmethod
    def from_json(cls, json: Dict[str,Any]):
        
        _code = json.get("code")
        _description = json.get("description")
        _id = json.get("id")
        _field = json.get("field")
        
        _new = cls(_code, _description, _id, _field)
        
        return _new
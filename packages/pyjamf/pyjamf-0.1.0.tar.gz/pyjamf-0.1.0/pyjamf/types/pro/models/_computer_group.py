
from pyrestsdk.type.model import Entity

class ComputerGroup(Entity):
    
    _id: int
    _name: str
    _is_smart_group: bool
    
    def __init__(self, client) -> None:
        super().__init__(client)
    
    @classmethod
    def from_json(cls, entry, client):
        
        _new = cls(client)
        
        _new._id = entry.get("id")
        _new._name = entry.get("name")
        _new._is_smart_group = entry.get("smartGroup")
        
        return _new
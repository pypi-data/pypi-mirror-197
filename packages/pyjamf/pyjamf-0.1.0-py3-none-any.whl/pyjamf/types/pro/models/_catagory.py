from ._entity import Entity

class Category(Entity):
    
    def __init__(self):
        super().__init__()
        self._name = ""
        self._priority = 0
    
    @property
    def Name(self) -> str:
        return self._name
    
    @property
    def Priority(self) -> int:
        return self._priority
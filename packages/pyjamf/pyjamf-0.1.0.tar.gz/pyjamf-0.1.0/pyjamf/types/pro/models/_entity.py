
class Entity(object):
    
    def __init__(self):
        self._id = ""
        
    @property
    def Id(self) -> str:
        return self._id

class AccountPreferences(object):
    
    def __init__(self):
        super().__init__()
        
        self._language = ""
        self._date_format = ""
        self._region = ""
        self._timezone = ""
        self._is_disable_relative_dates = False
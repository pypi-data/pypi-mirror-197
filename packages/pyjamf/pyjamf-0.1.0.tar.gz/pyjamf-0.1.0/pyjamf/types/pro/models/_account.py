from ._entity import Entity
from ._account_preferences import AccountPreferences

class Account(Entity):
    
    def __init__(self) -> None:
        super().__init__()
        self._username = ""
        self._real_name = ""
        self._email = ""
        self._preferences = AccountPreferences()
        self._is_multi_site_admin = False
        self._access_level = "" #[ FullAccess, SiteAccess, GroupBasedAccess ]
        self._privilege_set = "" #[ ADMINISTRATOR, AUDITOR, ENROLLMENT, CUSTOM ]
        self._privileges_by_site = []
        self._group_ids = []
        self._current_site_id = 0
        
    @property
    def Username(self) -> str:
        """Gets the Username

        Returns:
            str: The Username
        """
        return self._username
    
    @property
    def RealName(self) -> str:
        """Gets the real name

        Returns:
            str: The real name
        """
        return self._real_name
        
    @property
    def Email(self) -> str:
        """Gets the email

        Returns:
            str: The email
        """
        return self._email
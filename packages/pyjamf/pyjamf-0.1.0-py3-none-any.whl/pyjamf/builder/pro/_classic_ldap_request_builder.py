"""Houses Mobile Device Request Builder Type"""

from pyrestsdk.requestbuilder import BaseRequestBuilder

class ClassicLDAPRequestBuilder(BaseRequestBuilder):
    """Mobile Device Request Builder Type"""
    
    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """        
        super().__init__(request_url, client)
        
    def id(self, id: str):
        pass
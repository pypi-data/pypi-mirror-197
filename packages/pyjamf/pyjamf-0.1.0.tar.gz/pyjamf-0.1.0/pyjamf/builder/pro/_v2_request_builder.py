"""Houses Mobile Device Request Builder Type"""

from pyrestsdk.requestbuilder import BaseRequestBuilder

from pyjamf.builder.pro._mobile_devices_collection_request_builder import MobileDeviceCollectionRequestBuilder

class V2RequestBuilder(BaseRequestBuilder):
    """Mobile Device Request Builder Type"""
    
    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """        
        super().__init__(request_url, client)
        
    @property
    def cloud_ldaps(self):
        pass
    
    @property
    def computer_prestages(self):
        pass
    
    @property
    def enrollment(self):
        pass
    
    @property
    def enrollment_customizations(self):
        pass
    
    @property
    def inventory_preload(self):
        pass
    
    @property
    def jamf_pro_information(self):
        pass
    
    @property
    def mobile_devices(self) -> MobileDeviceCollectionRequestBuilder:
        
        return MobileDeviceCollectionRequestBuilder(self.append_segment_to_request_url("mobile-devices"), self.request_client)
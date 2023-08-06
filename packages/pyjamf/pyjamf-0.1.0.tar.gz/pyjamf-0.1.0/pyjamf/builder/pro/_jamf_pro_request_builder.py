"""Houses Jamf Pro Request Builder Type"""

from pyjamf.builder.pro._v1_request_builder import V1RequestBuilder
from pyjamf.builder.pro._v2_request_builder import V2RequestBuilder
from pyjamf.builder.pro._v3_request_builder import V3RequestBuilder

from pyrestsdk.requestbuilder import BaseRequestBuilder

class JamfProRequestBuilder(BaseRequestBuilder):
    """Jamf Pro Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)
        
    @property
    def v1(self) -> V1RequestBuilder:
        return V1RequestBuilder(self.append_segment_to_request_url("v1"), self.request_client)
    
    @property
    def v2(self) -> V2RequestBuilder:
        return V2RequestBuilder(self.append_segment_to_request_url("v2"), self.request_client)
    
    @property
    def v3(self) -> V3RequestBuilder:
        return V3RequestBuilder(self.append_segment_to_request_url("v2"), self.request_client)
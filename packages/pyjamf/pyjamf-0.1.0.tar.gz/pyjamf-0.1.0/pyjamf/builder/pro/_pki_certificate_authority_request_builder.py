"""Houses Mobile Device Request Builder Type"""

from pyrestsdk.requestbuilder import BaseRequestBuilder

from pyjamf.builder.pro._pki_certificate_authority_active_request_builder import PKICertificateAuthorityActiveRequestBuilder

class PKICertificateAuthorityRequestBuilder(BaseRequestBuilder):
    """Mobile Device Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def active(self) -> PKICertificateAuthorityActiveRequestBuilder:
        
        return PKICertificateAuthorityActiveRequestBuilder(self.append_segment_to_request_url("active"), self.request_client)
    
    def id(self, id: str):
        pass
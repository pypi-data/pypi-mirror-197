"""Houses Mobile Device Request Builder Type"""

from pyrestsdk.requestbuilder import BaseRequestBuilder

from pyjamf.builder.pro._pki_certificate_authority_active_der_request_builder import PKICertificateAuthorityActiveDerRequestBuilder
from pyjamf.builder.pro._pki_certificate_authority_active_pem_request_builder import PKICertificateAuthorityActivePemRequestBuilder


class PKICertificateAuthorityActiveRequestBuilder(BaseRequestBuilder):
    """Mobile Device Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)
        
    @property
    def der(self) -> PKICertificateAuthorityActiveDerRequestBuilder:
        
        return PKICertificateAuthorityActiveDerRequestBuilder(self.append_segment_to_request_url("der"), self.request_client)
    
    @property
    def pem(self) -> PKICertificateAuthorityActivePemRequestBuilder:
        
        return PKICertificateAuthorityActivePemRequestBuilder(self.append_segment_to_request_url("pem"), self.request_client)
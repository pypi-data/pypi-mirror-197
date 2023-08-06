"""Houses Mobile Device Request Builder Type"""

from pyrestsdk.requestbuilder import BaseRequestBuilder

from pyjamf.builder.pro._advanced_mobile_device_searches_request_builder import AdvancedMobileDeviceSearchesRequestBuilder
from pyjamf.builder.pro._advanced_user_content_searches_request_builder import AdvancedUserContentSearchesRequestBuilder
from pyjamf.builder.pro._app_dynamics_request_builder import AppDynamicsRequestBuilder
from pyjamf.builder.pro._computer_groups_request_builder import ComputerGroupsRequestBuilder


class V1RequestBuilder(BaseRequestBuilder):
    """Mobile Device Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)

    @property
    def advanced_mobile_device_searches(self) -> AdvancedMobileDeviceSearchesRequestBuilder:
        
        return AdvancedMobileDeviceSearchesRequestBuilder(self.append_segment_to_request_url("advanced-mobile-device-searches"), self.request_client)

    @property
    def advanced_user_content_searches(self) -> AdvancedUserContentSearchesRequestBuilder:
        
        return AdvancedUserContentSearchesRequestBuilder(self.append_segment_to_request_url("advanced-mobile-device-searches"), self.request_client)

    @property
    def app_dynamics(self) -> AppDynamicsRequestBuilder:
        
        return AppDynamicsRequestBuilder(self.append_segment_to_request_url("advanced-mobile-device-searches"), self.request_client)

    @property
    def app_request(self):
        pass

    @property
    def app_store_country_codes(self):
        pass

    @property
    def branding_images(self):
        pass

    @property
    def buildings(self):
        pass

    @property
    def cache_settings(self):
        pass

    @property
    def categories(self):
        pass

    @property
    def pki(self):
        pass

    @property
    def classic_ldap(self):
        pass

    @property
    def cloud_azure(self):
        pass

    @property
    def cloud_idp(self):
        pass

    @property
    def ldap_keystore(self):
        pass

    @property
    def computer_groups(self) -> ComputerGroupsRequestBuilder:
        
        return ComputerGroupsRequestBuilder(self.append_segment_to_request_url("computer-groups"), self.request_client)

    @property
    def computers_inventory(self):
        pass

    @property
    def computers_inventory_collection_settings(self):
        pass

    @property
    def conditional_access(self):
        pass

    @property
    def csa(self):
        pass

    @property
    def departments(self):
        pass

    @property
    def device_communication_settings(self):
        pass
    
    @property
    def device_enrollments(self):
        pass
    
    @property
    def ebooks(self):
        pass
    
    @property
    def engage(self):
        pass
    
    @property
    def adue_session_token_settings(self):
        pass
    
    @property
    def icon(self):
        pass
    
    @property
    def inventory_information(self):
        pass
    
    @property
    def jamf_connect(self):
        pass
    
    @property
    def jamf_management_framework(self):
        pass
    
    @property
    def jamf_package(self):
        pass
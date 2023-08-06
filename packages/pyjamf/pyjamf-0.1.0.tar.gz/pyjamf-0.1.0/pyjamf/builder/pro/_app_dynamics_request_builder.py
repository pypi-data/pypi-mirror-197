"""Houses Advanced Mobile Device Searches Choices Request Builder Type"""

from typing import Optional, Iterable

from pyrestsdk.requestbuilder import BaseRequestBuilder

from pyjamf.builder.pro._app_dynamics_script_configuration_request_builder import AppDynamicsScriptConfigurationRequestBuilder


class AppDynamicsRequestBuilder(BaseRequestBuilder):
    """Advanced Mobile Device Searches Choices Request Builder Type"""

    def __init__(self, request_url: str, client) -> None:
        """intializes a new DepartmentsRequestBuilder

        Args:
            request_url (str): the url to make the request to
            client (_type_): the client used to make the request
        """
        super().__init__(request_url, client)
        
    @property
    def script_configuration(self) -> AppDynamicsScriptConfigurationRequestBuilder:
        
        return AppDynamicsScriptConfigurationRequestBuilder(self.append_segment_to_request_url("script-configuration"), self.request_client, None)
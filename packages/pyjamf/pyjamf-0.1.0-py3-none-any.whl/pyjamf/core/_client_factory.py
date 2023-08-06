from requests import Session
import typing

#internal imports
from pyjamf.core.middleware.middleware import BaseMiddleware, MiddlewarePipeline
from .middleware.abc_token_credential import TokenCredential
from .middleware.authorization import AuthorizationHandler

class HTTPClientFactory:
    
    def __init__(self, hostname):
        
        self.session = Session()
        self._set_base_url(hostname)
        
    def create_with_default_middleware(self, credential: TokenCredential) -> Session:
        
        middleware = [
            AuthorizationHandler(credential),
            #RetryHandler()
        ]
        self._register(middleware)
        return self.session
        
    def _set_base_url(self, hostname):
        """Helper method to set the base url"""
        self.session.base_url = f"https://{hostname}.jamfcloud.com"
        
    def _register(self, middleware: typing.List[BaseMiddleware]) -> None:
        """
        Helper method that constructs a middleware_pipeline with the specified middleware
        """
        
        if middleware:
            middleware_pipeline = MiddlewarePipeline()
            for ware in middleware:
                middleware_pipeline.add_middleware(ware)
                
            self.session.mount('https://', middleware_pipeline)
from .abc_token_credential import TokenCredential
from .middleware import BaseMiddleware
from .._enums import FeatureUsageFlag

class AuthorizationHandler(BaseMiddleware):
    
    def __init__(self, credential: TokenCredential):
        super().__init__()
        self.credential = credential
        self.retry_count = 0
        
    def send(self, request, **kwargs):
        context = request.context
        request.headers.update(
            {'Authorization': 'Bearer {}'.format(self._get_access_token(context))}
        )
        
        context.set_feature_usage = FeatureUsageFlag.AUTH_HANDLER_ENABLED
        response = super().send(request)
        
        # Token might have expired just before transmission, retry the request one more time
        if response.status_code == 401 and self.retry_count < 2:
            self.retry_count += 1
            return self.send(request)
        return response
    
    def _get_access_token(self, context):
        return self.credential.get_token()
    
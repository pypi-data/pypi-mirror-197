from enum import Enum

class FeatureUsageFlag(int, Enum):
    """Enumerated list of values used to flag usage of specific middleware"""

    NONE = 0
    REDIRECT_HANDLER_ENABLED = 1
    RETRY_HANDLER_ENABLED = 2
    AUTH_HANDLER_ENABLED = 4
    DEFAULT_HTTP_PROVIDER_ENABLED = 8
    LOGGING_HANDLER_ENABLED = 16
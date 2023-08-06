class BaseAzureException(Exception):
    pass


class AzurePermissionsException(BaseAzureException):
    pass


class AzureTaskTimeoutException(BaseAzureException):
    pass


class InvalidAttrException(BaseAzureException):
    pass


class ResourceNotFoundException(BaseAzureException):
    pass


class MultipleResourceFoundException(BaseAzureException):
    pass


class NetworkNotFoundException(BaseAzureException):
    pass


class InvalidDiskTypeException(BaseAzureException):
    pass


class NoFreeDiskLunException(BaseAzureException):
    pass


class ReconfigureVMException(BaseAzureException):
    pass

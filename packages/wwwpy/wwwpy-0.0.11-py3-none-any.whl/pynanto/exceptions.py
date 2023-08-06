class PynantoException(Exception):
    pass


class RemoteException(PynantoException):
    """When user defined server code fails"""
    pass


class RemoteError(PynantoException):
    """When network/pynanto infrastructure fails"""
    pass

class VisepointError(Exception):
    """
    Base class for Visepoint errors.
    """
    pass

class VisepointInvalidCredentialsError(VisepointError):
    """
    Raised when the provided credentials are invalid.
    """
    def __init__(self, message="Invalid credentials provided."):
        self.message = message
        super().__init__(self.message)

class VisepointNotAuthorizedError(VisepointError):
    """
    Raised when the user is not authorized to perform the requested action.
    """
    def __init__(self, message="User is not authorized to perform this action."):
        self.message = message
        super().__init__(self.message)

class VisepointCreateError(VisepointError):
    """
    Raised when an error occurs while creating a resource.
    """
    def __init__(self, message="Error creating resource."):
        self.message = message
        super().__init__(self.message)

class VisepointAPIError(VisepointError):
    """
    Raised when an unexpected error occurs with the API.
    """
    def __init__(self, message="Unexpected error with API."):
        self.message = message
        super().__init__(self.message)

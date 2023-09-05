class FastGateException(Exception):
    """Base exception class for aiofastgate."""
    pass

class LoginFailed(FastGateException):
    """Raised when login fails for unknown reasons."""
    pass

class InvalidCredentials(FastGateException):
    def __init__(self, username: bool, password: bool) -> None:
        super().__init__(f"Invalid credentials: username valid: {username}, password valid: {password}")
    """Raised when login fails due to invalid credentials."""
    pass

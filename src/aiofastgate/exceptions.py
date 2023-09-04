class LoginFailed(Exception):
    """Raised when login fails for unknown reasons."""
    pass

class InvalidCredentials(Exception):
    def __init__(self, username: bool, password: bool) -> None:
        super().__init__(f"Invalid credentials: username valid: {username}, password valid: {password}")
    """Raised when login fails due to invalid credentials."""
    pass

class UserNotFoundException(Exception):

    def __init__(self, detail: str = "User not found."):
        self.detail = detail

class Authorized(Exception):
    """
    Authorized exception
    """

    def __init__(self, code: str = "0", message: str = "Authorized error."):
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"Error code: {self.code} -> {self.message}."


class ValueNotInRange(Exception):
    """
    Value exception
    """

    def __init__(self, message: str = "Value not in range."):
        self.message = message

    def __str__(self) -> str:
        return "%s." % self.message


class ModeNotExists(Exception):
    """
    Work mode exception
    """

    def __init__(self, mode: str = None, message: str = "Mode not exists"):
        self.mode = mode
        self.message = message

    def __str__(self):
        return f"Mode: {self.mode} -> {self.message}."

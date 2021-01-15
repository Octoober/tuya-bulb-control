class __MainException(Exception):
    def __init__(self, target: str, msg: str = ""):
        self.target = target
        self.msg = msg

    def __str__(self):
        return f"{self.target} -> {self.msg}"


class ModeNotSupported(__MainException):
    def __init__(self, target: str, msg: str = "Mode not supported your device."):
        self.target = target
        self.msg = msg


class FunctionNotSupported(__MainException):
    def __init__(self, target: str, msg: str = "Function not supported your device."):
        self.target = target
        self.msg = msg


class ArgumentError(__MainException):
    def __init__(self, target: str, msg: str = "Argument error."):
        self.target = target
        self.msg = msg


class AuthorizedError(__MainException):
    def __init__(self, target: str, msg: str = "Authorized error."):
        self.target = target
        self.msg = msg

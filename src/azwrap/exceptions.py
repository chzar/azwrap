class AzRequestError(Exception):
    pass

class AzParserError(Exception):
    pass

class AzResourceNotFoundError(Exception):
    pass

class AzUnsupportedCommand(Exception):
    pass

class AzCommandSyntaxError(Exception):
    def __init__(self, stderr: str):
        self.__stderr = stderr

    def __str__(self) -> str:
        return self.__stderr
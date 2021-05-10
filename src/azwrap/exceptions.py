class AzError(Exception):
    def __init__(self, stdout:str, stderr: str):
        self.__stdout = stdout
        self.__stderr = stderr

    @property
    def stdout(self):
        return self.__stdout

    @property
    def stderr(self):
        return self.__stderr
    
    def __str__(self) -> str:
        return self.stderr

class AzRequestError(AzError):
    def __init__(self, stdout: str, stderr: str):
        super().__init__(stdout, stderr)

class AzParserError(AzError):
    def __init__(self, stdout: str, stderr: str):
        super().__init__(stdout, stderr)

class AzResourceNotFoundError(AzError):
    def __init__(self, stdout: str, stderr: str):
        super().__init__(stdout, stderr)

class AzUnsupportedCommand(AzError):
    def __init__(self, stdout: str, stderr: str):
        super().__init__(stdout, stderr)

class AzCommandSyntaxError(AzError):
    def __init__(self, stdout: str, stderr: str):
        super().__init__(stdout, stderr)
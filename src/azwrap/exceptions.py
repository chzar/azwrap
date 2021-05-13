from types import List

class AzError(Exception):
    def __init__(self, stdout:str, stderr: str, commands: List(str)):
        self.__stdout = stdout
        self.__stderr = stderr
        self.__commands = commands

    @property
    def stdout(self):
        return self.__stdout

    @property
    def stderr(self):
        return self.__stderr
    
    @property
    def commands(self):
        return self.__commands

    def __str__(self) -> str:
        return f'[commands]: {self.commands}\n[stderr]:\n{self.stderr}'

class AzRequestError(AzError):
    def __init__(self, stdout: str, stderr: str, commands: List(str)):
        super().__init__(stdout, stderr, commands)

class AzParserError(AzError):
    def __init__(self, stdout: str, stderr: str, commands: List(str)):
        super().__init__(stdout, stderr, commands)

class AzResourceNotFoundError(AzError):
    def __init__(self, stdout: str, stderr: str, commands: List(str)):
        super().__init__(stdout, stderr, commands)

class AzUnsupportedCommand(AzError):
    def __init__(self, stdout: str, stderr: str, commands: List(str)):
        super().__init__(stdout, stderr, commands)

class AzCommandSyntaxError(AzError):
    def __init__(self, stdout: str, stderr: str, commands: List(str)):
        super().__init__(stdout, stderr, commands)
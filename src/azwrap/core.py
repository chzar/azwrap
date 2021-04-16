import sys
import os
import json
from pathlib import Path
from types import SimpleNamespace
from enum import Enum
from contextlib import redirect_stderr, redirect_stdout 
from io import StringIO
from azure.cli.core import get_default_cli
from pyfakefs.fake_filesystem_unittest import Patcher, fake_filesystem

UNSUPPORTED_COMMANDS = ["login"]

class DeploymentScope(Enum):
    Subscription = 0
    ResourceGroup = 1

class AzRequestError(Exception):
    pass
class AzParserError(Exception):
    pass
class AzResourceNotFoundError(Exception):
    pass
class AzCommandSyntaxError(Exception):
    pass
class AzUnsupportedCommand(Exception):
    pass

class Az:
    def __init__(self):
        self._cli = get_default_cli()
    def run(self, commands: list[str], options_dict=dict(), ignore_errors=False):
        if commands[0].lower() in UNSUPPORTED_COMMANDS:
            raise AzUnsupportedCommand

        for k, v in options_dict.items():
            commands.append('--' + k)
            commands.append(v)

        res = list()
        buf = StringIO()
        stdout_buf = StringIO()
        stderr_buf = StringIO()
        return_code = 0

        # Running invoke will always raise the SystemExit exception
        # Need to isolate it in a try-catch block
        try:
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                return_code = self._cli.invoke(commands, out_file=buf)
        except SystemExit:
            pass

        output = buf.getvalue()
        stdout = stdout_buf.getvalue()
        stderr = stderr_buf.getvalue()

        # The return code for command syntax errors is 0, so we will try to infer it
        if ( return_code == 0 
            and output == '' 
            and stdout == ''
            and stderr != '' ):
            return_code = 4 

        
        if not ignore_errors:
            if return_code == 1:
                raise AzRequestError
            elif return_code == 2:
                raise AzParserError
            elif return_code == 3:
                raise AzResourceNotFoundError
            elif return_code == 4:
                raise AzCommandSyntaxError


        try: 
            res = json.loads(output, object_hook=lambda item: SimpleNamespace(**item))
        except json.JSONDecodeError:
            pass
        return res

    def deploy(self, arm_template, scope: str, scope_type: DeploymentScope):
        fake_template_path = '/tempfs/arm_template'
        commands = ['deployment create',
                    'deployment group create -g {} -f {}'.format(scope, fake_template_path)]
        try: 
            arm_json = json.dumps(arm_template)
        except json.JSONDecodeError:
            pass

        with Patcher() as patcher:
            patcher.fs.add_real_directory(str(Path.home()))
            patcher.fs.create_file(fake_template_path, contents=arm_json)
            return self.run(commands[scope_type.value].split())
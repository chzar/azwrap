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
from typing import *
from azwrap.exceptions import AzRequestError, AzUnsupportedCommand, AzParserError, AzCommandSyntaxError, AzResourceNotFoundError

_unsupported_commands = ["login"]

_error_dict = {
            1: AzRequestError,
            2: AzParserError,
            3: AzResourceNotFoundError,
            4: AzCommandSyntaxError
        }

class DeploymentScope(Enum):
    Subscription = 0
    ResourceGroup = 1

class Az:
    def __init__(self):
        self._cli = get_default_cli()
    def run(self, commands_str: List[str], options_dict: Dict(str, str) = {}, ignore_errors=False):
        commands = commands_str.split()
        if commands[0].lower() in _unsupported_commands:
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

        # raise errors if applicable
        if not ignore_errors and return_code != 0:
            raise _error_dict[return_code](stdout, stderr)

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
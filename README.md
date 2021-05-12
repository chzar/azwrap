# Introduction
azwrap is the "ez" wrapper for az-cli!

Are you a Cloud engineer that:
* Is tired of the awkward powershell and az cli mish-mash?
* Wants a Pythonic way of managing Azure infrastructure?
* Wants seamless access to the many, high quality client libraries in the Python ecosystem (such as Kubenetes Python Client for managing AKS)?
* Wants to use mature templating libraries such as Jinja2 with ARM / Bicep templates to get similar functionality to helm charts?

Then ask your doctor if azwrap is right for you!

# Basic Usage
```python
from azwrap import *

tmpl = '{
            "name": "vnet2",
            "type": "Microsoft.Web/sites/virtualNetworkConnections",
            "location": "<Location>",
            "properties": {
                "vnetResourceId": "/subscriptions/<subscription id>/resourceGroups/<resource group>/providers/Microsoft.Network/virtualNetworks/<VNet>"
            }
        }
'

az = Az()

# create 'shortcut' functions
get_account = lambda: az.run('account show'.split()).id

# get account id
account_id = az.run('account show').id

# pass in cmdline options in a dictionary
output = az.run('network vnet create', options_dict={'name': 'vnet1', 'resource-group': 'MyResourceGroup'})

# deploy an arm template in code
vnet2_deployment = az.deploy(tmpl, 'MyResourceGroup', DeploymentScope.ResourceGroup)

# returned objects are lists and SimpleNamespace objects
first_rg = az.run('group list')[0].name

# error handling
try:
    print(az.run("group lt"))
except AzCommandSyntaxError as e:
    print(e.stdout)
    print(e.stderr)
```

# Pipeline Example
The below example is boilerplate code for making azwrap work in Azure DevOps Pipelines.

Most of the library dependencies are already available on the agents, but you will need to set your PYTHONPATH var so that pip and the python interpreter can find them.

After that you can use the AzureCLI task to call your python script or use the below HEREDOC example to write an inline script.


```
pool:
  vmImage: ubuntu-latest

variables:
- name: PYTHONPATH
  value: /opt/az/lib/python3.6/site-packages/

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.8.9'
    addToPath: true
    architecture: 'x64'
- task: Bash@3
  inputs:
    targetType: 'inline'
    script: |
      wget https://github.com/chzar/azwrap/releases/download/v0.3/azwrap-0.3.tar.gz
      python -m pip --upgrade pip
      python -m pip install azwrap-0.3.tar.gz
- task: AzureCLI@2
  inputs:
    azureSubscription: '###REDACTED###'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      python <(cat <<HEREDOC
      from azwrap import *

      az = Az()
      print(az.run('group list'))
      HEREDOC
      )
```

# Is azwrap Production Ready?
azwrap does not modify any of az-cli's functionality; it simply provides a pythonic way to use az cli. In theory, using azwrap is relatively safe but, it is not possible to exhaustively test azwrap. Usage of azwrap is at your own risk!

# azure-devops-python-samples

Azure DevOps Python SDK samples and helper scripts

## pushdownParentWorkItemCharacteristics

Take values from a defined set of fields and push values from parent to child e.g. transfer AreaPath or IterationPath from Bug to child Tasks.

```shell
./pushdownParentWorkItemCharacteristics.py '-o' 'https://dev.azure.com/{azure-devops-org}' '-t' '{azure-devops-pat}' '-p' '{azure-devops-project} --parent-type 'Bug' --child-type 'Task' --field-list 'System.AreaPath,System.IterationPath'
```

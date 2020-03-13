# azure-devops-python-samples

Azure DevOps Python SDK samples and helper scripts

> DISCLAIMER: Use these scripts with utmost care and at your own risk!
> By default the scripts only list the potential updates. Add `--update` flag for committing the update.

## pushdownParentWorkItemCharacteristics

Take values from a defined set of fields and push values from parent to child e.g. transfer AreaPath or IterationPath from Bug to child Tasks.

```shell
./pushdownParentWorkItemCharacteristics.py '-o' 'https://dev.azure.com/{azure-devops-org}' '-t' '{azure-devops-pat}' '-p' '{azure-devops-project} --parent-type 'Bug' --child-type 'Task' --field-list 'System.AreaPath,System.IterationPath'
```

## pushdownParentCompletedState

Push parent work items completed state to direct non-completed child work items.

```shell
./pushdownParentCompletedState.py '-o' 'https://dev.azure.com/{azure-devops-org}' '-t' '{azure-devops-pat}' '-p' '{azure-devops-project} --parent-type 'Feature' --child-type 'Product Backlog Item'
```

## rollupChildrenCompletedState

Roll up child work items completed state to to non-completed parent work items.

```shell
./rollupChildrenCompletedState.py '-o' 'https://dev.azure.com/{azure-devops-org}' '-t' '{azure-devops-pat}' '-p' '{azure-devops-project} --parent-type 'Feature' --child-type 'Product Backlog Item'
```

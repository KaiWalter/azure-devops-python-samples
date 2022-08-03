# azure-devops-python-samples

Azure DevOps Python SDK samples and helper scripts

---

> DISCLAIMER: Use these scripts with utmost care and at your own risk!
> By default the scripts only list the potential updates. Add `--update` flag for committing the update.

---

> These scripts refrain from using any kind of deep module or class structure so that the proposed functionality can be found in one place.

---

## pushdownParentWorkItemCharacteristics

Take values from a defined set of fields and push values from parent to child e.g. transfer AreaPath or IterationPath from Bug to child Tasks.

```shell
./pushdownParentWorkItemCharacteristics.py '-o' 'https://dev.azure.com/{azure-devops-org}' '-t' '{azure-devops-pat}' '-p' '{azure-devops-project} --parent-type 'Bug' --child-type 'Task' --field-list 'System.AreaPath,System.IterationPath'
```

Use flag `--update-all` to actually commit an update to all child work items and `--update-not-completed` to update all not yet completed child work items.

## pushdownParentCompletedState

Push parent work items completed state to direct non-completed child work items.

```shell
./pushdownParentCompletedState.py '-o' 'https://dev.azure.com/{azure-devops-org}' '-t' '{azure-devops-pat}' '-p' '{azure-devops-project} --parent-type 'Feature' --child-type 'Product Backlog Item'
```

Use flag `--update` to actually commit an update to child work items.

## rollupChildrenCompletedState

Roll up child work items completed state to to non-completed parent work items.

```shell
./rollupChildrenCompletedState.py '-o' 'https://dev.azure.com/{azure-devops-org}' '-t' '{azure-devops-pat}' '-p' '{azure-devops-project} --parent-type 'Feature' --child-type 'Product Backlog Item'
```

Use flag `--update` to actually commit an update to child work items.

---

## Python virtual environment setup

### for Windows

```PowerShell
python -m pip install --upgrade pip
pip3 install virtualenv
python -m virtualenv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\activate.ps1
pip install -r .\requirements.txt
```
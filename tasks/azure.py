from ast import literal_eval
from invoke import task
from subprocess import check_output, run


RESOURCE_GROUP = "faasm"
LOCATION = "eastus"

def _do_storage_account_get_key(name):
    _az_cmd = [
        "az",
        "storage account keys list",
        "--resource-group {}".format(RESOURCE_GROUP),
        "--account-name {}".format(name),
    ]

    az_cmd = " ".join(_az_cmd)
    print(az_cmd)

    _out = check_output(az_cmd, shell=True).decode("utf-8")
    out = literal_eval(_out)[0]["value"]
    return out

@task
def storage_account_get_key(ctx, name):
    """
    Get key1 to access the storage account
    """
    key = _do_storage_account_get_key(name)
    print(key)

@task
def storage_account_create(ctx, name, sku="Standard_LRS"):
    """
    Create storage account
    """
    _az_cmd = [
        "az",
        "storage account create",
        "--resource-group {}".format(RESOURCE_GROUP),
        "--name {}".format(name),
        "--sku {}".format(sku)
    ]

    az_cmd = " ".join(_az_cmd)
    print(az_cmd)

    run(az_cmd, shell=True, check=True)

@task
def storage_account_delete(ctx, name):
    """
    Delete storage account
    """
    _az_cmd = [
        "az",
        "storage account delete",
        "--resource-group {}".format(RESOURCE_GROUP),
        "--name {}".format(name),
    ]

    az_cmd = " ".join(_az_cmd)
    print(az_cmd)

    run(az_cmd, shell=True, check=True)

@task
def storage_container_create(ctx, name):
    """
    Delete storage account
    """
    _az_cmd = [
        "az",
        "storage container create",
        "--resource-group {}".format(RESOURCE_GROUP),
        "--account-name {}".format(name),
        "--account-key {}".format(_do_storage_account_get_key(name)),
        "--name storage",
    ]

    az_cmd = " ".join(_az_cmd)
    print(az_cmd)

    run(az_cmd, shell=True, check=True)

@task
def storage_container_delete(ctx, name):
    """
    Delete storage account
    """
    _az_cmd = [
        "az",
        "storage container delete",
        "--resource-group {}".format(RESOURCE_GROUP),
        "--account-name {}".format(name),
        "--account-key {}".format(_do_storage_account_get_key(name)),
        "--name storage",
    ]

    az_cmd = " ".join(_az_cmd)
    print(az_cmd)

    run(az_cmd, shell=True, check=True)

@task
def aks_create_cluster(ctx, name, node_count=5, vm_size="Standard_DS2_v2"):
    """
    Create a k8s cluster with Azure's Kubernetes Service
    """
    _az_cmd = [
        "az",
        "aks create",
        "--resource-group {}".format(RESOURCE_GROUP),
        "--name {}".format(name),
        "--node-count {}".format(node_count),
        "--node-vm-size {}".format(vm_size),
        "--generate-ssh-keys" 
    ]

    az_cmd = " ".join(_az_cmd)
    print(az_cmd)

    run(az_cmd, shell=True, check=True)


@task
def aks_get_credentials(ctx, name):
    """
    Get credentials for a new cluster
    """
    _az_cmd = [
        "az",
        "aks get-credentials",
        "--resource-group {}".format(RESOURCE_GROUP),
        "--name {}".format(name),
    ]

    az_cmd = " ".join(_az_cmd)
    print(az_cmd)

    run(az_cmd, shell=True, check=True)
    
    print("kubectl get nodes")
    run("kubectl get nodes", shell=True, check=True)


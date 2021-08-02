from ast import literal_eval
from invoke import task
from subprocess import check_output, run
from tasks.util.env import (
    AZURE_RESOURCE_GROUP,
    AZURE_REGION,
    AZURE_STORAGE_SKU,
    AZURE_VM_SIZE,
    AKS_CLUSTER_NODE_COUNT,
)


def _get_account_key(name):
    cmd = [
        "az",
        "storage account keys list",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--account-name {}".format(name),
    ]

    cmd = " ".join(cmd)
    print(cmd)

    out = check_output(cmd, shell=True).decode("utf-8")
    out = literal_eval(out)[0]["value"]
    return out


@task
def account_key(ctx, name):
    """
    Get key to access the storage account
    """
    key = _get_account_key(name)
    print(key)


@task
def create_account(ctx, name, sku=AZURE_STORAGE_SKU):
    """
    Create storage account
    """
    cmd = [
        "az",
        "storage account create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
        "--sku {}".format(sku),
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def delete_account(ctx, name):
    """
    Delete storage account
    """
    cmd = [
        "az",
        "storage account delete",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def create_container(ctx, name):
    """
    Create storage container
    """
    cmd = [
        "az",
        "storage container create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--account-name {}".format(name),
        "--account-key {}".format(_get_account_key(name)),
        "--name storage",
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def delete_container(ctx, name):
    """
    Delete storage account
    """
    cmd = [
        "az",
        "storage container delete",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--account-name {}".format(name),
        "--account-key {}".format(_get_account_key(name)),
        "--name storage",
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)

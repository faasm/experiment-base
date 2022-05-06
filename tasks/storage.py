from ast import literal_eval
from invoke import task
from subprocess import check_output, run
from tasks.util.env import (
    AZURE_REGION,
    AZURE_RESOURCE_GROUP,
    AZURE_STORAGE_SKU,
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
def account_create(ctx, name, sku=AZURE_STORAGE_SKU, location=AZURE_REGION):
    """
    Create storage account
    """
    cmd = [
        "az",
        "storage account create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
        "--sku {}".format(sku),
        "--location {}".format(AZURE_REGION),
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def account_delete(ctx, name):
    """
    Delete storage account
    """
    cmd = [
        "az",
        "storage account delete",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
        "--yes",
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def container_create(ctx, account_name, container_name):
    """
    Create storage container
    """
    cmd = [
        "az",
        "storage container create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--account-name {}".format(account_name),
        "--account-key {}".format(_get_account_key(account_name)),
        "--name {}".format(container_name),
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def container_delete(ctx, account_name, container_name):
    """
    Delete storage account
    """
    cmd = [
        "az",
        "storage container delete",
        "--account-name {}".format(account_name),
        "--account-key {}".format(_get_account_key(account_name)),
        "--name {}".format(container_name),
    ]

    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def container_file_upload(ctx, account_name, container_name, file_path):
    cmd = [
        "az storage blob upload",
        "--account-name {}".format(account_name),
        "--account-key {}".format(_get_account_key(account_name)),
        "--container-name {}".format(container_name),
        "--file {}".format(file_path),
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)

    cmd = [
        "az storage blob url",
        "--account-name {}".format(account_name),
        "--account-key {}".format(_get_account_key(account_name)),
        "--container-name {}".format(container_name),
    ]

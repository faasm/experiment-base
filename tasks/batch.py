from invoke import task
from subprocess import run

from tasks.storage import create_account as create_storage_account
from tasks.storage import delete_account as delete_storage_account
from tasks.util.env import (
    AZURE_BATCH_ACCOUNT_NAME,
    AZURE_BATCH_NODE_AGENT_SKU_ID,
    AZURE_BATCH_NODE_COUNT,
    AZURE_BATCH_POOL_ID,
    AZURE_BATCH_REGION,
    AZURE_BATCH_VM_IMAGE,
    AZURE_BATCH_VM_SIZE,
    AZURE_RESOURCE_GROUP,
)


def get_storage_account_name(name=AZURE_BATCH_ACCOUNT_NAME):
    """
    Get the storage account name from the batch account name
    """
    return "{}storage".format(name)


@task
def create_account(
    ctx, name=AZURE_BATCH_ACCOUNT_NAME, location=AZURE_BATCH_REGION
):
    """
    Creat account for and log in to Azure Batch
    """
    storage_account_name = get_storage_account_name(name)
    create_storage_account(ctx, storage_account_name)
    cmd = [
        "az batch account create",
        "--name {}".format(name),
        "--storage-account {}".format(storage_account_name),
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--location {}".format(location),
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)

    login_cmd = [
        "az batch account login",
        "--name {}".format(name),
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--shared-key-auth",
    ]

    login_cmd = " ".join(login_cmd)
    print(login_cmd)
    run(login_cmd, shell=True, check=True)


@task
def create_pool(
    ctx, node_count=AZURE_BATCH_NODE_COUNT, vm_size=AZURE_BATCH_VM_SIZE
):
    """
    Create node pool for the logged-in batch account
    """
    cmd = [
        "az batch pool create",
        "--id {}".format(AZURE_BATCH_POOL_ID),
        "--target-dedicated-nodes {}".format(node_count),
        "--vm-size {}".format(vm_size),
        "--image {}".format(AZURE_BATCH_VM_IMAGE),
        "--node-agent-sku-id '{}'".format(AZURE_BATCH_NODE_AGENT_SKU_ID),
        # The following are eeded for multi-node tasks (i.e. MPI)
        "--task-slots-per-node 1",
        "--enable-inter-node-communication",
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def pool_info(ctx):
    """
    Query Batch's node pool allocation state
    """
    cmd = [
        "az batch pool show",
        "--pool-id {}".format(AZURE_BATCH_POOL_ID),
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def delete_pool(ctx):
    """
    Delete Batch's node pool
    """
    cmd = [
        "az batch pool delete ",
        "--pool-id {}".format(AZURE_BATCH_POOL_ID),
        "--yes",
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def delete_account(
    ctx, name=AZURE_BATCH_ACCOUNT_NAME, location=AZURE_BATCH_REGION
):
    """
    Delete Batcha account
    """
    storage_account_name = get_storage_account_name(name)
    delete_storage_account(ctx, storage_account_name)
    cmd = [
        "az batch account delete",
        "--name {}".format(name),
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--yes",
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)

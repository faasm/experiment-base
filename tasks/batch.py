from ast import literal_eval
from invoke import task
from subprocess import check_output, run

from tasks.storage import account_create as create_storage_account
from tasks.storage import account_delete as delete_storage_account
from tasks.storage import container_create as create_storage_container
from tasks.storage import container_delete as delete_storage_container
from tasks.storage import container_file_upload
from tasks.util.env import (
    AZURE_BATCH_ACCOUNT_NAME,
    AZURE_BATCH_JOB_NAME,  # todo - may change this to job prefix or stgh like that
    AZURE_BATCH_NODE_AGENT_SKU_ID,
    AZURE_BATCH_NODE_COUNT,
    AZURE_BATCH_POOL_ID,
    AZURE_BATCH_REGION,
    AZURE_BATCH_STORAGE_CONTAINERS,
    AZURE_BATCH_VM_IMAGE,
    AZURE_BATCH_VM_SIZE,
    AZURE_RESOURCE_GROUP,
)


# ---------- Auxiliary methods ---------


def get_storage_account_name(name=AZURE_BATCH_ACCOUNT_NAME):
    """
    Get the storage account name from the batch account name
    """
    return "{}storage".format(name)


@task
def create_io_storage_containers(ctx):
    """
    Create the blob storage containers for batch input/output
    """
    for c in AZURE_BATCH_STORAGE_CONTAINERS:
        create_storage_container(ctx, get_storage_account_name(), c)


@task
def delete_io_storage_containers(ctx):
    """
    Delete the blob storage containers for batch input/output
    """
    for c in AZURE_BATCH_STORAGE_CONTAINERS:
        delete_storage_container(ctx, get_storage_account_name(), c)


def _get_account_key(name=AZURE_BATCH_ACCOUNT_NAME):
    cmd = [
        "az",
        "batch account keys list",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
    ]

    cmd = " ".join(cmd)
    print(cmd)

    out = check_output(cmd, shell=True).decode("utf-8")
    out = literal_eval(out)["primary"]
    return out


# ---------- Batch account management ---------


@task
def account_create(
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
def account_delete(
    ctx, name=AZURE_BATCH_ACCOUNT_NAME, location=AZURE_BATCH_REGION
):
    """
    Delete batch account
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


# ---------- Node pool management ---------

# TODO - replace for 'az batch pool create --json-file batch.json'
@task
def pool_create(
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
        # This is just for the demo
        "--start-task-command-line {}".format(
            """'/bin/sh -c "apt-get update; apt-get -y install libcr-dev mpich2 mpich2-doc"'"""
        ),
        "--start-task-wait-for-success",
        "--start-task-run-elevated",
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)

    # Create also the storage containers for IO
    create_io_storage_containers(ctx)


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
def pool_delete(ctx):
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

    # Delete also the storage containers for IO
    delete_io_storage_containers(ctx)


# ---------- Job management ---------


@task
def job_create(ctx):
    """
    Create job
    """
    cmd = [
        "az batch job create",
        "--account-key {}".format(_get_account_key()),
        "--account-name {}".format(AZURE_BATCH_ACCOUNT_NAME),
        "--id {}".format(AZURE_BATCH_JOB_NAME),
        "--pool-id {}".format(AZURE_BATCH_POOL_ID),
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)
    # TODO TODO
    # Up next, add tasks to job


@task
def job_delete(ctx):
    """
    Delete job
    """
    cmd = [
        "az batch job delete",
        "--account-key {}".format(_get_account_key()),
        "--account-name {}".format(AZURE_BATCH_ACCOUNT_NAME),
        "--job-id {}".format(AZURE_BATCH_JOB_NAME),
        "--yes",
    ]

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


# ---------- Task management ---------


@task
def task_create(ctx):
    """
    Create a task for a job
    """
    # First upload the required files
    container_file_upload(ctx, get_storage_account_name(), "input", "./hellompi.cpp")

from invoke import task
from os.path import join, exists
from os import makedirs
from shutil import copy, rmtree
from subprocess import run
from datetime import datetime

from tasks.util.env import (
    BIN_DIR,
    GLOBAL_BIN_DIR,
    KUBECTL_BIN,
    AZURE_RESOURCE_GROUP,
    AZURE_REGION,
    AZURE_VM_ADMIN,
    AZURE_VM_IMAGE,
    AZURE_STANDALONE_VM_SIZE,
    AKS_CLUSTER_NODE_COUNT,
    AKS_CLUSTER_NAME,
)

from tasks.util.version import get_k8s_version


@task
def create(ctx):
    """
    Creates a single Azure VM
    """

    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    name = "faasm-vm-{}".format(timestamp)

    print(
        "Creating VM {}, size {}, region {}".format(
            name, AZURE_STANDALONE_VM_SIZE, AZURE_REGION
        )
    )

    cmd = [
        "az vm create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
        "--image {}".format(AZURE_VM_IMAGE),
        "--admin-username {}".format(AZURE_VM_ADMIN),
        "--size {}".format(AZURE_STANDALONE_VM_SIZE),
        "--generate-ssh-keys",
    ]
    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)


@task
def delete(ctx, name):
    """
    Deletes the given Azure VM
    """
    pass


@task
def delete_all(ctx, name):
    """
    Deletes all the Azure VMs
    """
    pass


@task
def list(ctx):
    """
    List all Azure VMs
    """
    cmd = [
        "az vm list",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
    ]
    cmd = " ".join(cmd)
    print(cmd)

    run(cmd, shell=True, check=True)

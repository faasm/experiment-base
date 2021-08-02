from invoke import task
from subprocess import run
from tasks.util.env import (
    AZURE_RESOURCE_GROUP,
    AZURE_VM_SIZE,
    AKS_CLUSTER_NODE_COUNT,
    AKS_CLUSTER_NAME,
)

# AKS commandline reference here:
# https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest


def run_aks_cmd(name, az_args=None):
    cmd = [
        "az",
        "aks {}".format(name),
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
    ]

    if az_args:
        cmd.extend(az_args)

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def list(ctx):
    """
    List all AKS clusters
    """
    run_aks_cmd("list")


@task
def provision(ctx):
    """
    Provision the cluster
    """
    run_aks_cmd(
        "create",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
            "--node-count {}".format(AKS_CLUSTER_NODE_COUNT),
            "--node-vm-size {}".format(AZURE_VM_SIZE),
            "--generate-ssh-keys",
        ],
    )


@task
def details(ctx):
    """
    Show the details of the cluster
    """
    run_aks_cmd(
        "show",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
        ],
    )


@task
def delete(ctx):
    """
    Delete the cluster
    """
    run_aks_cmd(
        "delete",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
            "--yes",
        ],
    )


@task
def credentials(ctx, name):
    """
    Get credentials for the cluster
    """
    # Set up the credentials
    run_aks_cmd("get-credentials", ["--name {}".format(name)])

    # Check we can access the cluster
    print("kubectl get nodes")
    run("kubectl get nodes", shell=True, check=True)

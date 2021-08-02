from invoke import task
from os import makedirs
from os.path import join
from subprocess import run
from tasks.util.version import get_k8s_version
from tasks.util.env import (
    PROJ_ROOT,
    KUBECTL_BIN,
    AZURE_RESOURCE_GROUP,
    AZURE_VM_SIZE,
    AKS_CLUSTER_NODE_COUNT,
    AKS_CLUSTER_NAME,
)

# AKS commandline reference here:
# https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest


def _run_aks_cmd(name, az_args=None):
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
    List all AKS resources
    """
    _run_aks_cmd("list")


@task
def provision(ctx):
    """
    Provision the cluster
    """
    k8s_ver = get_k8s_version()

    _run_aks_cmd(
        "create",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
            "--node-count {}".format(AKS_CLUSTER_NODE_COUNT),
            "--node-vm-size {}".format(AZURE_VM_SIZE),
            "--kubernetes-version {}".format(k8s_ver),
            "--generate-ssh-keys",
        ],
    )


@task
def details(ctx):
    """
    Show the details of the cluster
    """
    _run_aks_cmd(
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
    _run_aks_cmd(
        "delete",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
            "--yes",
        ],
    )


@task
def credentials(ctx):
    """
    Get credentials for the cluster
    """
    # Set up the credentials
    _run_aks_cmd(
        "get-credentials",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
        ],
    )

    # Check we can access the cluster
    cmd = "{} get nodes".format(KUBECTL_BIN)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def install_kubectl(ctx):
    kubectl_dir = join(PROJ_ROOT, "bin")
    makedirs(kubectl_dir, exist_ok=True)

    k8s_ver = get_k8s_version()
    url = "https://dl.k8s.io/release/v{}/bin/linux/amd64/kubectl".format(
        k8s_ver
    )

    cmd = "curl -LO {}".format(url)
    run(cmd, shell=True, check=True, cwd=kubectl_dir)
    run("chmod +x kubectl", shell=True, check=True, cwd=kubectl_dir)

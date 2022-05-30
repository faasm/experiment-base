from invoke import task
from subprocess import run

from tasks.util.env import (
    KUBECTL_BIN,
    AZURE_RESOURCE_GROUP,
    AZURE_PUB_SSH_KEY,
    AZURE_K8S_CLUSTER_NAME,
    AZURE_K8S_NODE_COUNT,
    AZURE_K8S_REGION,
    AZURE_K8S_VM_SIZE,
)

from tasks.util.version import get_k8s_version


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
def provision(
    ctx,
    nodes=AZURE_K8S_NODE_COUNT,
    vm=AZURE_K8S_VM_SIZE,
    location=AZURE_K8S_REGION,
    sgx=False,
):
    """
    Provision the AKS cluster
    """
    k8s_ver = get_k8s_version()

    if sgx and "Standard_DC" not in vm:
        print(
            "Error provisioning SGX cluster: only `Standard_DC` VMs are supported"
        )
        return

    _run_aks_cmd(
        "create",
        [
            "--name {}".format(AZURE_K8S_CLUSTER_NAME),
            "--node-count {}".format(nodes),
            "--node-vm-size {}".format(vm),
            "--os-sku Ubuntu",
            "--kubernetes-version {}".format(k8s_ver),
            "--ssh-key-value {}".format(AZURE_PUB_SSH_KEY),
            "--location {}".format(location),
            "{}".format(
                "--enable-addons confcom --enable-sgxquotehelper"
                if sgx
                else ""
            ),
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
            "--name {}".format(AZURE_K8S_CLUSTER_NAME),
        ],
    )


@task
def delete(ctx):
    """
    Delete the AKS cluster
    """
    _run_aks_cmd(
        "delete",
        [
            "--name {}".format(AZURE_K8S_CLUSTER_NAME),
            "--yes",
        ],
    )


@task
def credentials(ctx):
    """
    Get credentials for the AKS cluster
    """
    # Set up the credentials
    _run_aks_cmd(
        "get-credentials",
        [
            "--name {}".format(AZURE_K8S_CLUSTER_NAME),
            "--overwrite-existing",
        ],
    )

    # Check we can access the cluster
    cmd = "{} get nodes".format(KUBECTL_BIN)
    print(cmd)
    run(cmd, shell=True, check=True)

from invoke import task
from os.path import join
from os import makedirs, remove
from shutil import copy, rmtree
from subprocess import run

from faasmcli.tasks.knative import KNATIVE_VERSION

from tasks.util.env import (
    BIN_DIR,
    KUBECTL_BIN,
    AZURE_RESOURCE_GROUP,
    AZURE_VM_SIZE,
    AKS_CLUSTER_NODE_COUNT,
    AKS_CLUSTER_NAME,
)
from tasks.util.version import get_k8s_version

# AKS commandline reference here:
# https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest

K9S_VERSION = "0.24.15"


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


def _download_binary(url, binary_name):
    makedirs(BIN_DIR, exist_ok=True)
    cmd = "curl -LO {}".format(url)
    run(cmd, shell=True, check=True, cwd=BIN_DIR)
    run("chmod +x {}".format(binary_name), shell=True, check=True, cwd=BIN_DIR)


@task
def install_kubectl(ctx):
    """
    Installs the k8s CLI (kubectl)
    """
    k8s_ver = get_k8s_version()
    url = "https://dl.k8s.io/release/v{}/bin/linux/amd64/kubectl".format(
        k8s_ver
    )
    _download_binary(url, "kubectl")


@task
def install_kn(ctx):
    """
    Installs the knative CLI (kn)
    """
    url = "https://github.com/knative/client/releases/download/v{}/kn-linux-amd64".format(
        KNATIVE_VERSION
    )
    _download_binary(url, "kn-linux-amd64")

    # Symlink for kn command
    run("ln -s kn-linux-amd64 kn", shell=True, check=True, cwd=BIN_DIR)


@task
def install_k9s(ctx):
    """
    Installs the K9s CLI
    """
    tar_name = "k9s_Linux_x86_64.tar.gz"
    url = "https://github.com/derailed/k9s/releases/download/v{}/{}".format(
        K9S_VERSION, tar_name
    )

    # Download the TAR
    workdir = "/tmp/k9s"
    makedirs(workdir, exist_ok=True)

    cmd = "curl -LO {}".format(url)
    run(cmd, shell=True, check=True, cwd=workdir)

    # Untar
    run("tar -xf {}".format(tar_name), shell=True, check=True, cwd=workdir)

    # Copy k9s into place
    copy(join(workdir, "k9s"), join(BIN_DIR, "k9s"))

    # Remove tar
    rmtree(workdir)

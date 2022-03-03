from invoke import task
from os.path import join, exists
from os import makedirs
from shutil import copy, rmtree
from subprocess import run

from tasks.util.env import (
    BIN_DIR,
    GLOBAL_BIN_DIR,
    KUBECTL_BIN,
    AZURE_RESOURCE_GROUP,
    AZURE_PUB_SSH_KEY,
    AZURE_K8S_CLUSTER_NAME,
    AZURE_K8S_NODE_COUNT,
    AZURE_K8S_REGION,
    AZURE_K8S_VM_SIZE,
)
from tasks.util.version import get_k8s_version

# Note - this must match the version used by Faasm
KNATIVE_VERSION = "1.1.0"
K9S_VERSION = "0.24.15"


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
            "{}".format("--enable-addons confcom" if sgx else ""),
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
    Delete the AKS cluster
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
    Get credentials for the AKS cluster
    """
    # Set up the credentials
    _run_aks_cmd(
        "get-credentials",
        [
            "--name {}".format(AKS_CLUSTER_NAME),
            "--overwrite-existing",
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

    return join(BIN_DIR, binary_name)


def _symlink_global_bin(binary_path, name):
    global_path = join(GLOBAL_BIN_DIR, name)
    if exists(global_path):
        print("Removing existing binary at {}".format(global_path))
        run(
            "sudo rm -f {}".format(global_path),
            shell=True,
            check=True,
        )

    print("Symlinking {} -> {}".format(global_path, binary_path))
    run(
        "sudo ln -s {} {}".format(binary_path, name),
        shell=True,
        check=True,
        cwd=GLOBAL_BIN_DIR,
    )


@task
def install_kubectl(ctx, system=False):
    """
    Install the k8s CLI (kubectl)
    """
    k8s_ver = get_k8s_version()
    url = "https://dl.k8s.io/release/v{}/bin/linux/amd64/kubectl".format(
        k8s_ver
    )

    binary_path = _download_binary(url, "kubectl")

    # Symlink for kubectl globally
    if system:
        _symlink_global_bin(binary_path, "kubectl")


@task
def install_kn(ctx, system=False):
    """
    Install the knative CLI (kn)
    """
    url = "https://github.com/knative/client/releases/download/knative-v{}/kn-linux-amd64".format(
        KNATIVE_VERSION
    )
    binary_path = _download_binary(url, "kn-linux-amd64")

    # Symlink for kn command locally
    run("rm -f kn", shell=True, check=True, cwd=BIN_DIR)
    run("ln -s {} kn".format(binary_path), shell=True, check=True, cwd=BIN_DIR)

    # Symlink for kn command globally
    if system:
        _symlink_global_bin(binary_path, "kn")


@task
def install_k9s(ctx, system=False):
    """
    Install the K9s CLI
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
    binary_path = join(BIN_DIR, "k9s")
    copy(join(workdir, "k9s"), binary_path)

    # Remove tar
    rmtree(workdir)

    # Symlink for k9s command globally
    if system:
        _symlink_global_bin(binary_path, "k9s")

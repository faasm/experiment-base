from invoke import task
from subprocess import run

from tasks.util.env import (
    KUBECTL_BIN,
    PROJ_ROOT,
)


@task
def reset(ctx):
    """
    Reset the uk8s cluster from scratch
    """
    # Delete existing .kube config directory
    rm_cmd = "sudo snap remove microk8s"
    print(rm_cmd)
    run(rm_cmd, shell=True, check=True)

    # Create new .kube config directory
    install_cmd = "./bin/install_microk8s.sh"
    print(install_cmd)
    run(install_cmd, cwd=PROJ_ROOT, shell=True, check=True)

    # Update credentials
    credentials(ctx)


@task
def credentials(ctx):
    """
    Set credentials for the uk8s cluster
    """
    # Delete existing .kube config directory
    del_cmd = "sudo rm -rf ~/.kube"
    print(del_cmd)
    run(del_cmd, shell=True, check=True)

    # Create new .kube config directory
    mkdir_cmd = "mkdir -p ~/.kube"
    print(mkdir_cmd)
    run(mkdir_cmd, shell=True, check=True)

    # Load the local config
    config_cmd = "sudo microk8s config > ~/.kube/config"
    print(config_cmd)
    run(config_cmd, shell=True, check=True)

    # Check we can access the cluster
    cmd = "{} get nodes".format(KUBECTL_BIN)
    print(cmd)
    run(cmd, shell=True, check=True)

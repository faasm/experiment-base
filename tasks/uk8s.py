from invoke import task
from subprocess import run

from tasks.util.env import KUBECTL_BIN


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

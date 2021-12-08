from invoke import task
from os.path import join
from subprocess import run

SHELL_IMG_NAME = "mcr.microsoft.com/aks/fundamental/base-ubuntu:v0.0.11"


def _run_kubectl_cmd(args):
    cmd = [
        "kubectl",
    ]
    cmd.extend(args)

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


# 08/12/21 - To SSH into a node in an AKS pool, we follow Microsoft's tutorial:
# https://docs.microsoft.com/en-us/azure/aks/ssh
@task
def ssh_node(ctx, node):
    """
    Get an SSH shell in a node in the AKS cluster node pool
    """
    cmd = [
        "debug",
        "node/{}".format(node),
        "-it --image={}".format(SHELL_IMG_NAME),
    ]

    _run_kubectl_cmd(cmd)

from invoke import task
from subprocess import run, PIPE, STDOUT
from datetime import datetime
import json

from tasks.util.env import (
    AZURE_PUB_SSH_KEY,
    AZURE_SSH_KEY,
    AZURE_RESOURCE_GROUP,
    AZURE_REGION,
    AZURE_VM_ADMIN,
    AZURE_VM_IMAGE,
    AZURE_STANDALONE_VM_SIZE,
)


@task
def create(ctx, region=AZURE_REGION):
    """
    Creates a single Azure VM
    """

    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    name = "faasm-vm-{}".format(timestamp)

    print(
        "Creating VM {}, size {}, region {}".format(
            name, AZURE_STANDALONE_VM_SIZE, region
        )
    )

    cmd = [
        "az vm create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
        "--image {}".format(AZURE_VM_IMAGE),
        "--admin-username {}".format(AZURE_VM_ADMIN),
        "--size {}".format(AZURE_STANDALONE_VM_SIZE),
        "--ssh-key-value {}".format(AZURE_PUB_SSH_KEY),
        "--location {}".format(region),
    ]
    cmd = " ".join(cmd)
    print(cmd)

    res = run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if res.returncode == 0:
        print(res.stdout)
        res = json.loads(res.stdout)

        print("\nTo SSH:")
        print(
            "ssh -A -i {} {}@{}".format(
                AZURE_SSH_KEY, AZURE_VM_ADMIN, res["publicIpAddress"]
            )
        )
    else:
        print(res.stderr)
        print(res.stdout)
        raise RuntimeError("Failed to provision VM")


def _list_all_vms():
    cmd = [
        "az vm list",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
    ]
    cmd = " ".join(cmd)

    res = run(cmd, shell=True, check=True, stdout=PIPE, stdin=PIPE)

    res = json.loads(res.stdout)
    print("Found {} VMs".format(len(res)))

    return res


def _vm_op(op, name, extra_args=None):
    print("Performing {} on {}".format(op, name))

    cmd = [
        "az vm {}".format(op),
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
    ]

    if extra_args:
        cmd.extend(extra_args)

    cmd = " ".join(cmd)
    print(cmd)
    run(cmd, shell=True, check=True)


@task
def start(ctx, name):
    """
    Starts (powers on) the given Azure VM.
    """
    _vm_op("start", name, ["--no-wait"])


@task
def deallocate(ctx, name):
    """
    Deallocates, i.e. powers down and deallocates compute resource for the
    given Azure VM so that it's not billed.
    """
    _vm_op("stop", name)


@task
def delete(ctx, name):
    """
    Deletes the given Azure VM
    """
    _vm_op("delete", name, ["--yes"])


@task
def delete_all(ctx):
    """
    Deletes all the Azure VMs
    """
    res = _list_all_vms()
    for vm in res:
        _vm_op("delete", vm["name"], ["--yes"])


@task
def list(ctx):
    """
    List all Azure VMs
    """
    res = _list_all_vms()
    for vm in res:
        print(
            "{}: {} {}".format(
                vm["name"],
                vm["location"],
                vm["hardwareProfile"]["vmSize"],
            )
        )


@task
def ip(ctx, name):
    """
    Show the IP details of a given VM
    """

    cmd = [
        "az vm list-ip-addresses",
        "-n {}".format(name),
        "-g {}".format(AZURE_RESOURCE_GROUP),
    ]

    cmd = " ".join(cmd)
    res = run(cmd, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

    res = json.loads(res.stdout)
    vm_info = res[0]["virtualMachine"]
    print(vm_info["network"]["publicIpAddresses"][0]["ipAddress"])

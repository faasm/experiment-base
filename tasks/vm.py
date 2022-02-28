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
    AZURE_SGX_VM_IMAGE,
    AZURE_SGX_VM_SIZE,
)

# Network components to be deleted, order matters
VM_NET_COMPONENTS = [
    ("nic", "VMNic"),
    ("nsg", "NSG"),
    ("vnet", "VNET"),
    ("public-ip", "PublicIp"),
]


def _get_ip(name):
    cmd = [
        "az vm list-ip-addresses",
        "-n {}".format(name),
        "-g {}".format(AZURE_RESOURCE_GROUP),
    ]

    cmd = " ".join(cmd)
    res = run(cmd, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

    res = json.loads(res.stdout)
    vm_info = res[0]["virtualMachine"]
    return vm_info["network"]["publicIpAddresses"][0]["ipAddress"]


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


def _vm_op(op, name, extra_args=None, capture=False):
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

    if capture:
        res = run(cmd, shell=True, check=True, stdout=PIPE, stderr=PIPE)
        return res.stdout.decode("utf-8")
    else:
        run(cmd, shell=True, check=True)


def _build_ssh_command(ip_addr):
    return "ssh -A -i {} {}@{}".format(AZURE_SSH_KEY, AZURE_VM_ADMIN, ip_addr)


@task
def create(ctx, region=AZURE_REGION, sgx=False, name=None):
    """
    Creates a single Azure VM
    """
    if not name:
        timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
        name = "faasm-vm{}-{}".format("-sgx" if sgx else "", timestamp)

    print(
        "Creating VM {}, size {}, region {}".format(
            name, AZURE_STANDALONE_VM_SIZE, region
        )
    )

    cmd = [
        "az vm create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
        "--admin-username {}".format(AZURE_VM_ADMIN),
        "--location {}".format(region),
        "--ssh-key-value {}".format(AZURE_PUB_SSH_KEY),
    ]

    if sgx:
        cmd.extend(
            [
                "--image {}".format(AZURE_SGX_VM_IMAGE),
                "--size {}".format(AZURE_SGX_VM_SIZE),
            ]
        )
    else:
        cmd.extend(
            [
                "--image {}".format(AZURE_VM_IMAGE),
                "--size {}".format(AZURE_STANDALONE_VM_SIZE),
            ]
        )

    cmd = " ".join(cmd)
    print(cmd)

    res = run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if res.returncode == 0:
        res = json.loads(res.stdout)

        print("\nTo SSH:")
        print(_build_ssh_command(res["publicIpAddress"]))
    else:
        print(res.stderr)
        print(res.stdout)
        raise RuntimeError("Failed to provision VM")


@task
def ssh(ctx, name):
    """
    Prints SSH information for given VM
    """
    ip_addr = _get_ip(name)
    print("--- SSH command ---\n")
    print(_build_ssh_command(ip_addr))

    print("\n--- SSH config ---")
    print(
        """
# Faasm SGX VM
Host {}
HostName {}
User {}
ForwardAgent yes
        """.format(
            name, ip_addr, AZURE_VM_ADMIN
        )
    )


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
    # Get OS disk name
    disk_out = _vm_op(
        "show",
        name,
        [
            "--query storageProfile.osDisk.managedDisk.id",
        ],
        capture=True,
    )
    os_disk = disk_out.split("/")[-1][:-2]

    # Delete the VM itself
    _vm_op("delete", name, ["--yes"])

    # Delete OS disk
    delete_disk_cmd = [
        "az disk delete",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(os_disk),
        "--yes",
    ]

    delete_disk_cmd = " ".join(delete_disk_cmd)
    print(delete_disk_cmd)
    run(
        delete_disk_cmd,
        check=True,
        shell=True,
    )

    # Delete all the network components
    for component, suffix in VM_NET_COMPONENTS:
        cmd = [
            "az",
            "network {}".format(component),
            "delete",
            "--resource-group {}".format(AZURE_RESOURCE_GROUP),
            "--name {}{}".format(name, suffix),
        ]

        cmd = " ".join(cmd)
        print(cmd)
        run(cmd, shell=True, check=True)


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
    ip = _get_ip()
    print(ip)

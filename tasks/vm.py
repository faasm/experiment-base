from invoke import task
from subprocess import run, PIPE, STDOUT
from os import makedirs
from os.path import exists
from datetime import datetime
import json

from tasks.util.ansible import run_ansible_playbook

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
    INVENTORY_DIR,
    INVENTORY_FILE,
    KUBECTL_REMOTE_PORT,
    FAASM_INVOKE_PORT,
    FAASM_UPLOAD_PORT,
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


def _list_all_vms(prefix=None):
    cmd = [
        "az vm list",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
    ]
    cmd = " ".join(cmd)

    res = run(cmd, shell=True, check=True, stdout=PIPE, stdin=PIPE)

    res = json.loads(res.stdout)

    if prefix:
        res = [v for v in res if v["name"].startswith(prefix)]
        print("Found {} VMs with prefix {}".format(len(res), prefix))
    else:
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
def create(ctx, region=AZURE_REGION, sgx=False, name=None, n=1):
    """
    Creates Azure VMs
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

    if n > 1:
        cmd.append("--count {}".format(n))

    cmd = " ".join(cmd)
    print(cmd)

    if n > 1:
        # Just run the command if we're creating more than one. Can query info
        # later
        run(cmd, shell=True, check=True)
    else:
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
        delete(ctx, vm["name"])


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
    ip = _get_ip(name)
    print(ip)


@task
def setup(ctx):
    """
    Set up an individual VM with the basics
    """
    run_ansible_playbook("vm.yml")


@task
def ports(ctx, prefix=None):
    """
    Open ports for Faasm and kubectl on VMs
    """
    vms = _list_all_vms(prefix)

    ports = ",".join(
        [
            str(KUBECTL_REMOTE_PORT),
            str(FAASM_UPLOAD_PORT),
            str(FAASM_INVOKE_PORT),
        ]
    )

    # Some default rules are created with priority 1000, which we have to avoid
    priority = 1500

    for i, vm in enumerate(vms):
        _vm_op(
            "open-port",
            vm["name"],
            extra_args=[
                "--port {}".format(ports),
                "--priority {}".format(priority),
            ],
        )


@task
def inventory(ctx, prefix=None):
    """
    Create ansbile inventory for VMs
    """
    all_vms = _list_all_vms(prefix)

    if len(all_vms) == 0:
        print("Did not find any VMs matching prefix {}".format(prefix))
        raise RuntimeError("No VMs found with prefix")

    print("Generating inventory for {} VMs".format(len(all_vms)))

    # Sort VMs based on name to ensure consistent choice of main
    all_vms = sorted(all_vms, key=lambda d: d["name"])

    # Get all IPs
    for vm in all_vms:
        vm["public_ip"] = _get_ip(vm["name"])

    if not exists(INVENTORY_DIR):
        makedirs(INVENTORY_DIR, exist_ok=True)

    main_vm = all_vms[0]
    other_vms = all_vms[1:]

    # One group for all VMs, one for main, one for workers
    lines = ["[all]"]
    for v in all_vms:
        # Include VM name for debugging purposes
        lines.append(
            "{} \tvm_name={}".format(
                v["public_ip"], v["name"]
            )
        )

    lines.append("\n[main]")
    lines.append(main_vm["public_ip"])
    lines.append("\n[worker]")
    lines.extend([v["public_ip"] for v in other_vms])

    file_content = "\n".join(lines)

    print("Contents:\n")
    print(file_content)

    with open(INVENTORY_FILE, "w") as fh:
        fh.write(file_content)
        fh.write("\n")

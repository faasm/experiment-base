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
    K8S_INGRESS_PORT,
    K8S_NODEPORT_RANGE,
)


# Network components to be deleted, order matters
NSG_COMPONENT_CMD = "nsg"
VM_NET_COMPONENTS = [
    ("nic", "VMNic"),
    (NSG_COMPONENT_CMD, "NSG"),
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


@task(
    help={
        "n": "Number of VM instances",
        "name": "Name to be given to the VM(s)",
        "region": "Azure region",
        "sgx": "Enable SGX",
        "vm": "Azure VM type",
    }
)
def create(ctx, vm=None, region=AZURE_REGION, sgx=False, name=None, n=1):
    """
    Creates Azure VMs
    """

    # WARNING: we rely on a name ending in an integer to detect whether it's
    # been created by Azure in bulk. Therefore, don't have this base name end in
    # an integer
    if not name:
        timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
        name = "faasm-{}-{}-vm".format("-sgx" if sgx else "", timestamp)

    vm_image = AZURE_VM_IMAGE
    vm_type = AZURE_STANDALONE_VM_SIZE

    if vm:
        vm_type = vm
    elif sgx:
        vm_image = AZURE_SGX_VM_IMAGE
        vm_type = AZURE_SGX_VM_SIZE

    print(
        "Creating {} VMs: name={} type={} region={} image={}".format(
            n, name, vm_type, region, vm_image
        )
    )

    # Note here how we specify that we want to delete the associted resources:
    # https://docs.microsoft.com/en-us/azure/virtual-machines/delete?tabs=cli2
    cmd = [
        "az vm create",
        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
        "--name {}".format(name),
        "--admin-username {}".format(AZURE_VM_ADMIN),
        "--location {}".format(region),
        "--ssh-key-value {}".format(AZURE_PUB_SSH_KEY),
        "--image {}".format(vm_image),
        "--size {}".format(vm_type),
        "--public-ip-sku Standard",
        "--os-disk-delete-option delete",
        "--data-disk-delete-option delete",
        "--nic-delete-option delete",
    ]

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

    # If we've created VMs in bulk, they will have slightly different naming
    # conventions to those created individually.
    # If created in bulk, Azure will have added an extra integer to the end of
    # the name, which we can look for

    # The need for this function is suprirising, it would be nice if the az
    # delete command could just delete everything for us. Discussion here:

    last_char = name[-1]
    is_bulk = last_char.isnumeric()

    if is_bulk:
        bulk_idx = last_char
        bulk_base_name = name[:-1]

        print(
            "Assuming {} created in bulk (idx {}, base {})".format(
                name, bulk_idx, bulk_base_name
            )
        )
    else:
        print("Assuming {} was not created in bulk".format(name))

        bulk_idx = None
        bulk_base_name = None

    # Get OS disk name
    #    disk_out = _vm_op(
    #        "show",
    #        name,
    #        [
    #            "--query storageProfile.osDisk.managedDisk.id",
    #        ],
    #        capture=True,
    #    )
    #    os_disk = disk_out.split("/")[-1][:-2]

    # Delete the VM itself
    _vm_op("delete", name, ["--yes"])

    # Delete OS disk


#    delete_disk_cmd = [
#        "az disk delete",
#        "--resource-group {}".format(AZURE_RESOURCE_GROUP),
#        "--name {}".format(os_disk),
#        "--yes",
#    ]

#    delete_disk_cmd = " ".join(delete_disk_cmd)
#    print(delete_disk_cmd)
#    run(
#        delete_disk_cmd,
#        check=True,
#        shell=True,
#    )

# Delete all the network components
#    for component, suffix in VM_NET_COMPONENTS:
#        fail_on_error = True
#
#        if is_bulk and component == NSG_COMPONENT_CMD:
#            # Azure create a single NSG for bulk-create VMs, so need to ignore
#            # failures if it doesn't exist
#            fail_on_error = False
#            component_name = bulk_base_name + suffix
#        elif is_bulk:
#            component_name = bulk_base_name + suffix + bulk_idx
#        else:
#            component_name = name + suffix
#
#        cmd = [
#            "az",
#            "network {}".format(component),
#            "delete",
#            "--resource-group {}".format(AZURE_RESOURCE_GROUP),
#            "--name {}".format(component_name),
#        ]
#
#        cmd = " ".join(cmd)
#        print(cmd)
#        run(cmd, shell=True, check=fail_on_error)


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
def open_ports(ctx, prefix=None):
    """
    Open ports for Faasm and kubectl on VMs
    """
    vms = _list_all_vms(prefix)

    ports = ",".join(
        [
            str(KUBECTL_REMOTE_PORT),
            str(FAASM_UPLOAD_PORT),
            str(FAASM_INVOKE_PORT),
            str(K8S_INGRESS_PORT),
            str(K8S_NODEPORT_RANGE),
        ]
    )

    # Some default rules are created with priority 1000, which we have to avoid
    priority = 1600

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
        lines.append("{} \tvm_name={}".format(v["public_ip"], v["name"]))

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

# Experiment setup with Azure

## Links

Here are some docs that may be useful when dealing with AKS:

- [Commandline
  reference](https://docs.microsoft.com/en-us/cli/azure/aks?view=azure-cli-latest)
- [AKS load
  balancers](https://docs.microsoft.com/en-us/azure/aks/load-balancer-standard)

## Azure CLI

You will need to set up the Azure client (`az`) as per the [official
instructions](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

In Ubuntu:

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Then run the Azure login:

```bash
az login
```

On success, this returns some JSON with the details of your account(s). You need
to pick the `id` field of the one you want, then:

```bash
az account set -s <account_id>
```

## Setting up a cluster with AKS

_At the time of writing, AKS only supported Ubuntu 18.04, which is insufficient
for certain experiments. See below for setting up a cluster on custom VMs._

Provision the cluster with:

```bash
inv cluster.provision
```

Once set up, you need to configure `kubectl` with:

```bash
inv cluster.credentials
```

From here you can follow the [Faasm k8s
instructions](https://faasm.readthedocs.io/en/latest/source/kubernetes.html)
from a normal Faasm checkout.

### Clearing up

Once finished with the cluster, you can delete it with:

```bash
inv cluster.delete
```

## Setting up VMs

List any in existence:

```bash
inv vm.list-all
```

Create a new one:

```bash
inv vm.create
```

Delete one:

```bash
# Delete a specific VM and associated resources
inv vm.delete <vm name>
```

Delete all:

```bash
# Delete all VMs and resources
inv vm.delete-all

# Delete all VMs and resources with given prefix
inv vm.delete-all --prefix <some prefix>
```

The size of VMs is determined in the script itself, so you can tweak it there if
necessary.

Once provisioned, you can set up a VM according to [the docs](docs/vms.md).

## Setting up K8s on custom VMs

Create as many VMs as you need:

```bash
inv vm.create -n 4
```

List them to work out which ones you want to deploy on:

```bash
inv vm.list-all
```

If you just want to deploy on all the ones that are there, you can run the
following commands without a prefix, otherwise deploy on a subset using their
shared name prefix.

We have to set up the Ansible inventory, and open the ports necessary for Faasm
and kubectl:

```bash
# All VMs
inv vm.open-ports
inv vm.inventory

# VMs with names starting with prefix
inv vm.open-ports --prefix <vm prefix>
inv vm.inventory --prefix <vm prefix>
```

You can then follow the [k8s setup docs](docs/k8s.md).

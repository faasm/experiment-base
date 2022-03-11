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
inv vm.list
```

Create a new one:

```bash
inv vm.create
```

Install basics:

```bash
inv vm.setup <vm_name>
```

Delete one:

```bash
inv vm.delete <vm_name>
```

Delete all:

```bash
inv vm.delete-all
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
inv vm.list
```

If you just want to deploy on all the ones that are there, you can run the
following commands without a prefix, otherwise deploy on a subset using their
shared name prefix.

We have to set up the Ansible inventory, and open the remote kubectl port:

```bash
# All VMs
inv vm.kubectl-port
inv vm.inventory

# VMs with names starting with prefix
inv vm.kubectl-port --prefix <vm prefix>
inv vm.inventory --prefix <vm prefix>
```

You can then follow the [k8s setup docs](docs/k8s.md).

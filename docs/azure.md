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

## Setting up a k8s cluster on Azure

Provision the cluster with:

```bash
inv cluster.provision
```

Once set up, you need to configure `kubectl` with:

```bash
inv cluster.credentials
```

From here you can follow the [Faasm k8s
instructions](https://github.com/faasm/faasm/blob/master/docs/kubernetes.md)
from a normal Faasm checkout.

### Clearing up

Once finished with the cluster, you can delete it with:

```bash
inv cluster.delete
```

## Creating a VM Scale Set Cluster

Note that these are only needed for running micro benchmarks.

To bootstrap the cluster run:

```bash
./az-vm/az_vms.sh create <NUM_VMS>
```

You will have to modify the script if you want to change the VM type.

To delete the cluster:

```bash
./az-vm/az_vms.sh delete
```

# Experiment setup with Azure

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

## Setting up Faasm on AKS

This repo contains tasks to provision the underlying K8s cluster:

```bash
inv cluster.provision
```

Once set up, you can check the cluster and that `kubectl` commands work with:

```bash
inv cluster.details
inv cluster.credentials
```

From here you can follow the [Faasm k8s
instructions](https://github.com/faasm/faasm/blob/master/docs/kubernetes.md).

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

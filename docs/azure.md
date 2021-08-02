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

## Kubectl

You also need to install the correct version of `kubectl` which can be done
using the task in this repo:

```bash
inv cluster.install-kubectl
```

Or you can check [`K8S_VERSION`](../K8S_VERSION) and do it yourself.

You then need to make sure that running `kubectl` from the shell gives the right
version:

```bash
cat K8S_VERSION
kubectl version
```

This should be the case if you've run `source bin/workon.sh` as described in
the setup for this repo.

## Provisioning with AKS

The [tutorial
docs](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-app)
give an overview.

This repo contains tasks to provision the cluster:

```bash
inv cluster.provision
```

Once set up, you can check the cluster and that `kubectl` commands work with:

```bash
inv cluster.details
inv cluster.credentials
```

You then need to install Knative with:

```bash
inv faasm.knative.install
```

Once finished, you can delete with:

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

## Creating a local microk8s cluster for development

[Official instructions](https://microk8s.io/).

Check with:

```bash
sudo microk8s status
sudo microk8s start # if not started
sudo microk8s kubectl get nodes
```

# Azure Configuration

## Commandline tools

You will need to set up the Azure client (`az`) as per the [official
instructions](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

In Ubuntu this boils down to:

```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

You will also need `kubectl` as described [here](
https://kubernetes.io/docs/tasks/tools/install-kubectl/).

## Login

First run the Azure login:

```bash
az login
```

On success, this returns some JSON with the details of your account(s). You need
to pick the `id` field of the one you want, then:

```bash
az account set -s <account_id>
```

## Provisioning with AKS

The [tutorial
docs](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-app)
give an overview.

This repo contains tasks to provision the cluster:

```bash
inv cluster.provision
```

Once set up, you can check with:

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

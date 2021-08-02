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

## K8s client `kubectl` and Knative client `kn`

You also need to install the correct versions of `kubectl` and `kn`, which can
be done using the tasks in this repo:

```bash
inv cluster.install-kubectl
inv cluster.install-kn
```

Check `kubectl` gives the right version with:

```bash
cat K8S_VERSION

kubectl version
```

Check `kn` is working with:

```bash
kn version
```

Note that both are installed in the `bin` directory of this repo, and should be
added to `PATH` via `source bin/workon.sh` as described in the main `README`.

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

You then need to install Knative on this cluster with:

```bash
inv faasm.knative.install
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

## Creating a local microk8s cluster for development

[Official instructions](https://microk8s.io/).

Check with:

```bash
sudo microk8s status
sudo microk8s start # if not started
sudo microk8s kubectl get nodes
```

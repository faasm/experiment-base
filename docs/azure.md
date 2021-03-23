# Azure Configuration

## Commandline tools

You will need to set up the Azure client (`az`) as per the 
[official instructions](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

In Ubuntu this boils down to:

```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

You will also need `kubectl` as described [here](
https://kubernetes.io/docs/tasks/tools/install-kubectl/).

## Login

```
az login
az account set -s <account ID>
```

You may need to be graned access first. 

## Provisioning a Kubernetes Cluster with AKS and Knative

```bash
az aks create \
  --resource-group faasm \
  --name <myClusterName> \
  --node-count <myClusterSize> \
  --node-vm-size <vmSize> \ # Default: Standard_DS2_v2
  --generate-ssh-keys 
```

You can check with:

```
# Check the cluster
az aks get-credentials --resource-group faasm --name <myClusterName>

# Check with kubectl
kubectl get nodes
```

Faasm runs on `knative` to install a minimal version of it run:
```
inv faasm.knative.install
```

## Creating a VM Scale Set Cluster

**Important: VM scale sets are EXPENSIVE. Make sure you delete the cluster once
you are done with it.**

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

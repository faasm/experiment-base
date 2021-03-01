# Experiments for Faabric Paper

This repository is the common entrypoint for all experiments in [faabric](
    https://github.com/faasm/faabric), as presented in the [paper](
    https://github.com/faasm/faabric-paper).

## Table of Contents

1. [Experiment Index](#experiment-index)
2. [Quick Start](#quick-start)
3. [First Time Users](#first-time-users)
4. [Creating a New Experiment](#new-experiment) 
5. [Cluster Provisioning](#cluster-provisioning)
6. [Troubleshooting](#troubleshooting)

## Experiment Index <a name="experiment-index">

| Name | Status | Results | Run Experiment |
| --- | --- | --- | --- |
| [LAMMPS](https://github.com/faasm/experiment-lammps) | :x: MPI Error | [Plots](https://github.com/faasm/experiment-lammps/plots/README.md) | [Instructions](https://github.com/faasm/experiment-lammps/README.md) |
| [ParRes Kernels](https://github.com/faasm/experiment-kernels) | :heavy_check_mark: Waiting Plot Spec | [Plots](https://github.com/faasm/experiment-kernels/plots/README.md) | [Instructions](https://github.com/faasm/experiment-kernels/README.md) |
| [PyWren](https://github.com/faasm/experiment-pywren) | :clock9: WIP | [Plots](https://github.com/faasm/experiment-pywren/plots/README.md) | [Instructions](https://github.com/faasm/experiment-pywren/README.md) |

## Quick Start <a name="quick-start">

If its the first time you are running these experiments, **you must first follow
the [instructions for first time users](#first-time-users)**.

Then, you may navigate to any of the experiments repository (see the [Experiment
Index](#experiment-index)) and run a specific experiment.

Alternatively, you may run all experiments in the paper by doing:
```
TODO: have a one-liner to run all the scripts prior to the artifact evaluation
```

## First Time Users <a name="first-time-users">

To run the experiments in the Azure cluster, you will need to set up the azure
client (`az`).

To install the client, follow the [official instructions](
  https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
If you are running on Ubuntu, the previous command will have you doing:
```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
(we include it here to avoid checking the link in the general case).

Then, you need to login to the LSDS cluster using the appropriate credentials.
Note that, in general, you will first need someone to grant you access.
```
az login # use IMP credentials
az account set -s e594b650-46d3-4375-be21-2ea11e8ed741
```
if any of the previous fails, open an issue in this repo and mention one of its
maintainers.

## Creating a new experiment <a name="new-experiment">

When creating a new experiment from scratch, there are a few steps you need to
take for seamless integration and automation with the current scheme.
First, you'll need to create a new repository under the [faasm org](
  https://github.com/faasm) following the pattern `experiment-<name>`.
Then, the recommended approach is to copy one of the existing repositories, and
see what you need to change.

In particular, you will need to do the following:

### Create Native and Faasm-compatible Dockerfiles

Experiments require _all_ code to be containerized in Docker containers.
For each experiment, you will need two different images: one for the native
(baseline) execution of the vanilla source, and a second one for the `Faasm`
compatible, WASM build.
It is encouraged that you create the following structure under your root dir.

## Cluster Provisioning <a name="cluster-provisioning">

The cluster needs to be provisioned only once. 
Check the Azure portal beforehand to see if everything is deployed before
running any of the following.
If it is the first time you are interacting with Azure through the command
line, make sure you've read the [first time users instructions](#first-time-users).

This section covers the following topics:
1. [Creating a Kubernetes Cluster at Azure using AKS](#aks-cluster)
2. [Creating a VM Cluster at Azure using VM Scale Sets](#vmss-cluster)
3. [Create a local microk8s Cluster for Development](#microk8s-cluster)

### Creating a Kubernetes Cluster using Azure Kubernetes Service (AKS) <a name="aks-cluster">

To create a k8s cluster using the Azure Kubernetes Service, run the following
command specifying the number of replicas you want:
```bash
az aks create \
  --resource-group faasm \
  --name <myClusterName> \
  --node-count <myClusterSize> \
  --node-vm-size <vmSize> \ # Default: Standard_DS2_v2
  --generate-ssh-keys 
```
You may now ensure that the cluster has been properly initialized by running:
```
az aks get-credentials --resource-group faasm --name <myClusterName>
```
and finally using `kubectl` ([installation instructions](
https://kubernetes.io/docs/tasks/tools/install-kubectl/)):
```
kubectl get nodes
```

### Creating a VM Scale Set Cluster <a name="vmss-cluster">

**Important: VM scale sets are EXPENSIVE. Make sure you delete the cluster once
you are done with it.**

We provide a set of convenience scripts to manage virtual machine (VM) clusters.
You can may inspect the [source code](
  https://github.com/faasm/experiment-base/blob/master/az-vm/az_vms.sh).
You will have to modify the sources if you want to change the VM type.
In particular, you will have to change the `--vm-sku` argument in `create`.

To bootstrap the cluster run:
```bash
./az-vm/az_vms.sh create <NUM_VMS>
```

You may now check through the portal that the cluster has been properly
initialized, together with necessary maintenance resources.
To delete the cluster just run:
```bash
./az-vm/az_vms.sh delete
```

### Creating a local microk8s cluster for development <a name="microk8s-cluster">

Microk8s acts as a local k8s cluster, and is a drop-in replacement for AKS.
It should be the preferred choice for development purposes.
To install it, follow the instructions [here](
  https://microk8s.io/).
Once done, test your deployment using:
```bash
sudo microk8s status
sudo microk8s start # if not started
sudo microk8s kubectl get nodes
```

## Troubleshooting <a name="troubleshooting">

In general, when facing any problem not listed below, open an issue in this
repository and make sure to tag one of its maintainers so that they can help
you in the debugging process.

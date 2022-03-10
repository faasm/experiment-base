# Kubernetes setup

## Kubectl

Install `kubectl` with:

```bash
inv k8s.install-kubectl --system
```

Note that this will place the binary in `/usr/local/bin`, to be available
globally. If you just want to use the installs with the tasks in this repo, you
can drop the `system` flag.

Check `kubectl` gives the right version with:

```bash
cat K8S_VERSION

which kubectl

kubectl version --client
```

## KNative client (kn)

Install with:

```bash
inv k8s.install-kn --system
```

Check `kn` is working with:

```bash
which kn

kn version
```

## K9s

To improve your QoL when using k8s, you can install
[`k9s`](https://github.com/derailed/k9s) too:

```bash
inv cluster.install-k9s --system

which k9s
```

## Setting up K8s on VMs

These instructions are only relevant if you're installing k8s on a cluster of
custom VMs. Managed k8s services like AKS will require their own specific setup
steps.

### Ansible inventory

You first need to set up an Ansible inventory containing the VMs you want to set
up K8s on. See `ansible/inventory/README.md`, or run the Azure-specific command
as described in [the Azure docs](docs/azure.md).

Check that Ansible can ping the vms:

```bash
inv k8s.host-ping
```

### Install

To install Ansible on the hosts listed in the inventory file:

```bash
inv k8s.install
```

This will install [microk8s](https://microk8s.io/), check out code, and set up
`kubectl` from the VM marked as `main` in your inventory file.


# Kubernetes setup

All the commands in this file assume you've set up the Python virtual
environment for this project as per the [README](README.md).

These instructions are just about setting up k8s tooling, if you have a cluster
set up with `kubectl` and `kn` working, you can follow the [Faasm k8s
docs](https://faasm.readthedocs.io/en/latest/source/kubernetes.html).

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

*Make sure that all of your VMs have the relevant kubectl port open to your
client machine*. You can check what this is using `kubectl config view` on one
of the VMs. `16443` is the default at the time of writing.

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

This will use the ansible playbooks defined in the `ansible` directory to
install and set up k8s, and check out our code.

This is performing a lot of setup and takes a while depending on the VM type.
If you see any errors, you can try just rerunning. If that fails, you may find
the ansible [troubleshooting
docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_startnstep.html#)
useful. You can also try nuking the `~/.ansible` directory and rerunning.

Once k8s is installed, you should be able to run the following to update your
config to run `kubectl`:

```bash
inv k8s.config
```

To check you can run:

```bash
kubectl get nodes
```

and should see your VMs.

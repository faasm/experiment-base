# Setting up K8s on VMs

## Ansible inventory

You first need to set up an Ansible inventory file at
`ansible/inventory/k8s.ini`, containing the VMs you want to set up K8s on.

There are commands to do this automatically for Azure VMs, see [the
docs](azure.md).

Check that Ansible can ping the vms:

```bash
inv k8s.host-ping
```

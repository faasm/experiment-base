# Running on individual VMs

First you need to pick your VM from the list:

```bash
inv vm.list-all
```

Then you need to update the Anisble inventory file:

```bash
inv vm.inventory --prefix <vm name>
```

Then you can run the following to install the basics:

```bash
inv vm.setup
```

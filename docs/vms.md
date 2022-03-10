# Running on individual VMs

To set up the basics, you first need to update the Anisble inventory file using
the associated command:

```bash
inv vm.inventory --prefix <vm name>
```

Then you can run:

```bash
inv vm.setup
```



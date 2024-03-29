# Running experiments locally

## Microk8s

[Official instructions](https://microk8s.io/).

We have to install the same version we'll be running the experiments on. This
can be done with:

```bash
./bin/install_microk8s.sh
```

Check with:

```bash
sudo microk8s status

# If not running
sudo microk8s start
```

Lastly, update the credentials for `kubectl` to point to the microk8s cluster:

```bash
inv uk8s.credentials
```

From here you can follow the [Faasm k8s
instructions](https://github.com/faasm/faasm/blob/main/docs/kubernetes.md) to
set up Faasm in the cluster.

Be careful to also add any instructions in there that are specific to MicroK8s.

### Resetting

The quickest way to completely reset the cluster is:

```bash
inv uk8s.reset
```

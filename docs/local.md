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

From here you can follow the [Faasm k8s
instructions](https://github.com/faasm/faasm/blob/master/docs/kubernetes.md) to
set up Faasm in the cluster.

Be careful to also add any instructions in there that are specific to MicroK8s
(e.g. installing `istio`, setting up `kubectl`).

Note that all Faasm `inv` commands can be run from this repo using the `faasm.`
prefix, e.g.

```bash
inv faasm.knative.install
```

### Resetting

The quickest way to completely reset the cluster is:

```bash
sudo snap remove microk8s
./bin/install_microk8s.sh
```

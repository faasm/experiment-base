# Running experiments locally

## Microk8s

[Official instructions](https://microk8s.io/).

Make sure you install the same version you'll be running the experiments on.
This has to be the 1.xx version shown in the `K8S_VERSION` file:

```bash
cat K8S_VERSION

K8S_MAJOR=<1.xx here>

sudo snap install microk8s --classic --channel=${K8S_MAJOR}/stable
```

Check with:

```bash
sudo microk8s status

# If not running
sudo microk8s start
```

From here you can follow the [Faasm k8s
instructions](https://github.com/faasm/faasm/blob/master/docs/kubernetes.md).

Be careful to also add any instructions in there that are specific to MicroK8s
(e.g. installing `istio`, setting up `kubectl`).


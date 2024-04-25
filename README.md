# Faabric Experiments

This repo contains the shared infrastructure for experiments related to
[Faasm](http://github.com/faasm/faasm) and
[Faabric](https://github.com/faasm/faabric).

To run all the experiments, you'll need to set up a Kubernetes cluster in a
cloud provider or locally:

- [Azure cluster setup](docs/azure.md).
- [Local cluster setup](docs/local.md).
- [Installing and configuring K8s](docs/k8s.md).

For a specific set of experiments, consider checking out the following repos:
- [Faabric experiments](https://github.com/faasm/experiment-faabric)
- [TLess experients](https://github.com/faasm/experiment-sgx)

## Setup

```bash
source ./bin/workon.sh

# List available tasks
inv -l
```


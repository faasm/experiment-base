# Faabric Experiments

This repo contains the shared infrastructure for experiments related to
[Faasm](http://github.com/faasm/faasm) and
[Faabric](https://github.com/faasm/faabric).

To run all the experiments, you'll need to set up a Kubernetes cluster in a
cloud provider or locally:

- [Azure cluster setup](docs/azure.md).
- [Local cluster setup](docs/local.md).
- [Installing and configuring K8s](docs/k8s.md).

## Setup

```bash
git submodule update --init

# Install the python dependencies
source bin/workon.sh
pip3 install -U pip
pip3 install -r requirements.txt

# List available tasks
inv -l
```


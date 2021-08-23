# Faabric Experiments

This repo contains the shared infrastructure for experiments related to
[Faasm](http://github.com/faasm/faasm) and
[Faabric](https://github.com/faasm/faabric).

To run all the experiments, you'll need to set up a Kubernetes cluster in a
cloud provider or locally:

- [Azure cluster setup](docs/azure.md).
- [Local cluster setup](docs/local.md).

Once you have a cluster, each experiment repo contains specific information on
how to run it:

- [MPI (LAMMPS and ParRes Kernels)](experiments/mpi/README.md)
- [OpenMP (Covid)](experiments/covid/README.md)

## Setup

```bash
git submodule update --init
cd faasm
git submodule update --init clients/cpp
cd ..

# Install the python dependencies
source bin/workon.sh
pip3 install -U pip
pip3 install -r requirements.txt

# List available tasks
inv -l
```

You also need to install the correct versions of `kubectl` and `kn`, which can
be done using the tasks in this repo:

```bash
inv cluster.install-kubectl
inv cluster.install-kn
```

Check `kubectl` gives the right version with:

```bash
cat K8S_VERSION

which kubectl

kubectl version --client
```

Check `kn` is working with:

```bash
which kn

kn version
```

Note that both are installed in the `bin` directory of this repo, and should
automatically be added to `PATH` via `source bin/workon.sh`.

You can optionally install [`k9s`](https://github.com/derailed/k9s) (for a nicer
`kubectl` experience) with:

```bash
inv cluster.install-k9s

which k9s
```

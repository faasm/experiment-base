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

- [MPI (LAMMPS and ParRes Kernels)](https://github.com/faasm/experiment-mpi)
- [OpenMP (Covid)](https://github.com/faasm/experiment-covid)
- [Microbenchmarks (Polybench and
  Python)](https://github.com/faasm/experiment-microbench)

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

You also need to install the correct versions of `kubectl` and `kn`, which can
be done using the tasks in this repo:

```bash
inv cluster.install-kubectl --system
inv cluster.install-kn --system
```

Note that this will place the `kubectl` and `kn` binaries into `/usr/local/bin`,
to be available globally. If you just want to use the installs with the tasks in
this repo, you can drop the `system` flag.

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

We also recommend that you install [`k9s`](https://github.com/derailed/k9s) too,
as it makes managing the cluster much easier than running `kubectl` all the
time.

```bash
inv cluster.install-k9s --system

which k9s
```

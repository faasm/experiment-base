# Faabric Experiments

This repo contains the shared infrastructure for experiments related to
[Faasm](http://github.com/faasm/faasm) and
[Faabric](https://github.com/faasm/faabric).

More info:

- [Azure setup](docs/azure.md).
- [Local setup](docs/local.md).
- [Setting up new experiments](docs/new_experiments.md).

Each experiment repo contains information on how to run that experiment:

- [LAMMPS](https://github.com/faasm/experiment-lammps)
- [ParRes Kernels](https://github.com/faasm/experiment-kernels)
- [PyWren](https://github.com/faasm/experiment-pywren)
- [Covid](https://github.com/faasm/experiment-covid)

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

kubectl version
```

Check `kn` is working with:

```bash
kn version
```

Note that both are installed in the `bin` directory of this repo, and should be
added to `PATH` via `source bin/workon.sh` as described in the main `README`.
To set up this repo:

You can optionally install [`k9s`](https://github.com/derailed/k9s) with:

```bash
inv cluster.install-k9s
```

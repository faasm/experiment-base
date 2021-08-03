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

To set up this repo:

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

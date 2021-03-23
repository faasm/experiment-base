# Faabric Experiments

This repository is a skeleton for the experiment repos for
[Faasm](http://github.com/faasm/faasm) and 
[Faabric](https://github.com/faasm/faabric).

For information on accessing and provisioning Azure resources see [the
docs](docs/azure.md).

If creating a new experiment, see [the docs](docs/new_experiments.md).

## Experiments

| Name | Plot Ready | Native Execution | Faasm Execution | Results | Run Experiment |
| --- | --- | --- | --- | -- | -- |
| [LAMMPS](https://github.com/faasm/experiment-lammps) | | :white_check_mark: | | [Plots](https://github.com/faasm/experiment-base/blob/master/plots/README.md) | [Instructions](https://github.com/faasm/experiment-lammps/blob/master/README.md) |
| [ParRes Kernels](https://github.com/faasm/experiment-kernels) | :white_check_mark: | :white_check_mark: | :white_check_mark: | [Plots](https://github.com/faasm/experiment-base/blob/master/results/kernels/README.md) | [Instructions](https://github.com/faasm/experiment-kernels/blob/master/README.md) |
| [PyWren](https://github.com/faasm/experiment-pywren) | | :white_check_mark: | | [Plots](https://github.com/faasm/experiment-master/blob/master/plots/README.md) | [Instructions](https://github.com/faasm/experiment-pywren/blob/master/README.md) |
| [Covid](https://github.com/faasm/experiment-covid) | | :white_check_mark: | | [Plots](https://github.com/faasm/experiment-base/blob/master/plots/README.md) | [Instructions](https://github.com/faasm/experiment-covid/blob/master/README.md) |

## Quick Start

To run the experiments, first clone this repository and install the
dependencies:
```bash
git clone https://github.com/faasm/experiment-base --recurse-submodules
./bin/here.sh
pip3 install -U pip
pip3 install -r requirements.txt
```

```
TODO: have a one-liner to run all the scripts prior to the artifact evaluation
```

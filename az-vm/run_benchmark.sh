#!/bin/bash

set -e

THIS_DIR=$(dirname $(readlink -f $0))
PROJ_DIR=${THIS_DIR}/..

pushd ${PROJ_DIR} >> /dev/null

# Experiment variables
ROOT_DIR=/code/experiment-kernels
CLUSTER_SIZE=5
MPI_PROCS_PER_NODE=2
echo "----------------------------------------"
echo "      Kernels Native VM Benchmark       "
echo "                                        "
echo "Benchmark parameters:                   "
echo "    - VM Cluster Size: ${CLUSTER_SIZE} "
echo "    - Max. MPI processes per node: ${MPI_PROCS_PER_NODE}"
echo "----------------------------------------"

# Deploy and resize cluster
# ./az-vm/az_vms.sh create
# ./az-vm/az_vms.sh scale ${CLUSTER_SIZE}
echo "----------------------------------------"

# Generate the ansible inventory
echo "Generating ansible inventory..."
./az-vm/gen_host_file.sh ansible

# Run the ansible playbook
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook \
    -i ./az-vm/ansible/inventory.yml \
    --become \
    ./az-vm/ansible/mpi_playbook.yml

# Generate the corresponding host file
MPI_MAX_PROC=${MPI_PROCS_PER_NODE} source ./az-vm/gen_host_file.sh
echo "----------------------------------------"

# Copy the run batch script just in case we have changed something (so that we
# don't have to rebuild the image)
scp ./run/all.py faasm@${MPI_MASTER}:/code/experiment-kernels/run/all.py

# Run the benchmark at the master
ssh faasm@${MPI_MASTER} "/code/experiment-kernels/run/all.py"
echo "----------------------------------------"

# Grep the results
mkdir -p ./results
scp faasm@${MPI_MASTER}:kernels_native_k8s_line.dat \
    ./results/kernels_native_vms_line.dat

popd >> /dev/null

# Plot them
# pushd plot >> /dev/null
# gnuplot lammps_native_k8s.gnuplot
# popd >> /dev/null

#!/bin/bash

set -e

THIS_DIR=$(dirname $(readlink -f $0))
PROJ_ROOT=${THIS_DIR}/..

pushd ${PROJ_ROOT} >> /dev/null

# Experiment variables
CLUSTER_SIZE=5
MPI_PROCS_PER_NODE=5
echo "----------------------------------------"
echo "      ${EXPERIMENT} k8s Benchmark       "
echo "                                        "
echo "Benchmark parameters:                   "
echo "    - K8s Cluster Size: ${CLUSTER_SIZE} "
echo "    - Max. MPI processes per node: ${MPI_PROCS_PER_NODE}"
echo "----------------------------------------"

# Generate the corresponding host file
MPI_MAX_PROC=${MPI_PROCS_PER_NODE} source ./uk8s/gen_host_file.sh
echo "----------------------------------------"

# Copy the run batch script just in case we have changed something (so that we
# don't have to rebuild the image)
sudo microk8s kubectl cp ${RUN_SCRIPT} ${MPI_MASTER}:/home/mpirun/all.py

# Run the benchmark at the master
sudo microk8s \
    kubectl exec -it \
    ${MPI_MASTER} -- bash -c "su mpirun -c '/home/mpirun/all.py'"
echo "----------------------------------------"

# Grep the results
mkdir -p ./results
sudo microk8s kubectl cp ${MPI_MASTER}:/home/mpirun/results.dat \
    ./results/${EXPERIMENT}.dat

# Delete leftovers
sudo microk8s \
    kubectl exec -it \
    ${MPI_MASTER} -- bash -c "rm /home/mpirun/results.dat"

popd >> /dev/null


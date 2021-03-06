#!/bin/bash

set -e

# See if the user has specified an env variable
MAX_PROC=${MPI_MAX_PROC:-"4"}
NAMESPACE="faabric"

# Generate the hostfile
kubectl \
    get pods -n ${NAMESPACE} -l run=faabric -o wide \
    | awk -v slots=${MAX_PROC} 'NR>1 {print $6" slots=" slots}' > hostfile

# SCPit to the first host
MPI_MASTER=$(kubectl -n ${NAMESPACE} get pods -l run=faabric | awk 'NR==2 {print $1}')
export MPI_MASTER=${MPI_MASTER}
echo "Chosen as master node w/ name: ${MPI_MASTER}"
kubectl cp hostfile ${NAMESPACE}/${MPI_MASTER}:/home/mpirun/hostfile

# Debug print and delete
echo "Copying generated hostfile to master:"
cat hostfile
rm hostfile


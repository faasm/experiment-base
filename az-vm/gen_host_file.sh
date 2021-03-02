#!/bin/bash

set -e

THIS_DIR=$(dirname $(readlink -f $0))
PROJ_DIR=${THIS_DIR}/..

pushd ${PROJ_DIR} >> /dev/null

if [[ $1 == "ansible" ]]; then
    # Generate the inventory file
    INV_FILE="./az-vm/ansible/inventory.yml"
    echo "[all]" > ${INV_FILE}
    ./az-vm/az_vms.sh ip | \
        awk 'NR>2 {print $2}' >> ${INV_FILE}

    echo "" >> ${INV_FILE}
    echo "[all:vars]" >> ${INV_FILE}
    echo "ansible_connection=ssh" >> ${INV_FILE}
    echo "ansible_user=faasm" >> ${INV_FILE}

    cat ${INV_FILE}
else
    # See if the user has specified an env variable
    MAX_PROC=${MPI_MAX_PROC:-"4"}

    # Generate the hostfile
    ./az-vm/az_vms.sh ip | \
        awk -v slots=${MAX_PROC} 'NR>2 {print $2" slots=" slots}' > hostfile

    # SCPit to the first host
    MPI_MASTER=$(./az-vm/az_vms.sh ip | awk 'NR==3 {print $2}')
    export MPI_MASTER=${MPI_MASTER}
    echo "Chosen as master node w/ name: ${MPI_MASTER}"
    ssh faasm@${MPI_MASTER} "mkdir -p /home/mpirun"
    scp hostfile faasm@${MPI_MASTER}:/home/mpirun/hostfile

    # Debug print and delete
    echo "Copying generated hostfile to master:"
    cat hostfile
    rm hostfile
fi

popd >> /dev/null


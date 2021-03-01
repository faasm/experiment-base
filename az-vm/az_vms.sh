#!/bin/bash

set -e

THIS_DIR=$(dirname $(readlink -f $0))
PROJ_DIR=${THIS_DIR}/..
CLUSTER_NAME="faasmVMcluster"

pushd ${PROJ_DIR} >> /dev/null

if [[ $1 == "create" ]]; then
    COUNT=${2:-1}
    echo "Creating the VM scale set with $COUNT VMs"
    az vmss create \
        --resource-group faasm \
        --name ${CLUSTER_NAME} \
        --image UbuntuLTS \
        --instance-count ${COUNT} \
        --vm-sku Standard_D2_v2 \
        --public-ip-per-vm \
        --admin-username faasm \
        --generate-ssh-keys
elif [[ $1 == "deallocate" ]]; then
    az vmss deallocate \
        --resource-group faasm \
        --name ${CLUSTER_NAME}
elif [[ $1 == "delete" ]]; then
    az vmss delete \
        --resource-group faasm \
        --name ${CLUSTER_NAME}
elif [[ $1 == "ip" ]]; then
    az vmss list-instance-public-ips \
        --resource-group faasm \
        --name ${CLUSTER_NAME} \
        --output table
elif [[ $1 == "list" ]]; then
    az vmss list-instances \
        --resource-group faasm \
        --name ${CLUSTER_NAME} \
        --output table
elif [[ $1 == "scale" ]]; then
    if [[ -z $2 ]]; then
        echo "You must specify the new capacity when running the scale command"
        echo "usage: ./az_vms.sh scale <new_capacity>"
        exit 1
    fi
    echo "Scaling cluster to $2 instances"
    az vmss scale \
        --resource-group faasm \
        --name ${CLUSTER_NAME} \
        --new-capacity $2
elif [[ $1 == "start" ]]; then
    echo "Starting the cluster instances"
    az vmss start \
        --resource-group faasm \
        --name ${CLUSTER_NAME} &
elif [[ $1 == "stop" ]]; then
    echo "Stopping the cluster instances"
    az vmss stop \
        --resource-group faasm \
        --name ${CLUSTER_NAME}
else
    echo "Unknown command: $1"
    echo "usage: ./az_vms.sh [create|delete|list|scale|start|stop]"
    exit 1
fi

popd >> /dev/null


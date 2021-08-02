#!/bin/bash

set -e

RESOURCE_GROUP="faasm"
CLUSTER_NAME="faasm-cluster"
NODE_COUNT=2
VM_SIZE="Standard_DS2_v2"

az aks create \
  --resource-group ${RESOURCE_GROUP} \
  --name ${CLUSTER_NAME} \
  --node-count ${NODE_COUNT} \
  --node-vm-size ${VM_SIZE} \
  --generate-ssh-keys

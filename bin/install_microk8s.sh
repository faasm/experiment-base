#!/bin/bash

set -e

K8S_VERSION=$(cat K8S_VERSION)
K8S_MAJOR=${K8S_VERSION:0:4}

echo "Installing microk8s version ${K8S_MAJOR}"

sudo snap install microk8s --classic --channel=${K8S_MAJOR}/stable

sudo microk8s.enable istio

#!/bin/bash

set -e
set -x

# ------------------------------------------------
# Minimal VM setup script. Assumes Ubuntu 20.04.
#
# This should be *just* the base setup needed to run the
# Dockerised Faasm environment and nothing more.
# ------------------------------------------------

sudo apt update
sudo apt upgrade -y

# Code
mkdir -p ~/code
pushd ~/code

export GIT_SSL_NO_VERIFY=true
git clone git@github.com:faasm/faasm.git
pushd faasm
git submodule update --init

popd
popd

# HWE
sudo apt install -y --install-recommends linux-generic-hwe-20.04

# Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

sudo apt-cache policy docker-ce
sudo apt install -y docker-ce

# Docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker ${USER}

# Done
echo ""
echo "Done. Now log out and in again to check things have worked."
echo ""

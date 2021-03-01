#!/bin/bash

set -e

THIS_DIR=$(dirname $(readlink -f $0))
DOCKER_DIR=${THIS_DIR}/..
PROJ_ROOT=${THIS_DIR}/../..

IMAGE_NAME="experiment-kernels"
VERSION="$(sed -n '2,2p' .env | cut -d"=" -f 2)"
FAASM_VERSION="$(head -1 ${PROJ_ROOT}/.env | cut -d"=" -f 2)"

pushd ${PROJ_ROOT} >> /dev/null

export DOCKER_BUILDKIT=1

# Docker args
NO_CACHE=$1

docker build \
    ${NO_CACHE} \
    -t faasm/${IMAGE_NAME}:${VERSION} \
    -f ${DOCKER_DIR}/${IMAGE_NAME}.dockerfile \
    --build-arg EXPERIMENTS_VERSION=${VERSION} \
    --build-arg FAASM_VERSION=${FAASM_VERSION} \
    --build-arg FORCE_RECREATE=$(date +%s) \
    ${PROJ_ROOT}

popd >> /dev/null


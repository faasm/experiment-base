#!/bin/bash

set -e

THIS_DIR=$(dirname $(readlink -f $0))
DOCKER_DIR=${THIS_DIR}/..
PROJ_ROOT=${THIS_DIR}/../..

IMAGE_NAME="experiment-base-native"
VERSION=$(cat ${PROJ_ROOT}/VERSION)

pushd ${PROJ_ROOT} >> /dev/null

export DOCKER_BUILDKIT=1

# Docker args
if [ "$1" == "--no-cache" ]; then
    NO_CACHE=$1
else
    NO_CACHE=""
fi

docker build \
    ${NO_CACHE} \
    -t faasm/${IMAGE_NAME}:${VERSION} \
    -f ${DOCKER_DIR}/${IMAGE_NAME}.dockerfile \
    --build-arg FORCE_RECREATE=$(date +%s) \
    ${PROJ_ROOT}

if [ "${BASH_ARGV[0]}" == "--push" ]; then
    docker push faasm/${IMAGE_NAME}:${VERSION}
fi

popd >> /dev/null


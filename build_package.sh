#!/bin/bash

# A short script which build wheel pcakage for fisheye using docker
# USAGE : ./build_package.sh [output dir | -h]

IMAGE_NAME=adet_build
CONTAINER_NAME=adet_builder
CONTAINER_DEST=/usr/src/app/dist
HOST_DEST="$(pwd)"
PYTHON=py38
FLAVOUR=$1

VERSION=$PYTHON-$FLAVOUR

container="${CONTAINER_NAME}-${VERSION}"
image="${IMAGE_NAME}-${VERSION}"

# remove old build container if remaining from previous failed run
docker rm ${container}

echo "docker build -t "${image}" -f "./docker/Dockerfile-$VERSION" ."
docker build -t "${image}" -f "./docker/Dockerfile-$VERSION" .
if ! [ $? -eq 0 ] ; then
    echo "[KO] Unable to build docker for python-$PYTHON" >&2
    exit 1
fi

echo "docker run --name ${container} ${image}"
docker run --name ${container} ${image}
if ! [ $? -eq 0 ] ; then
    echo "[KO] Unable to build package, no such file or directory" >&2
    exit 1
fi

echo "docker cp $container:$CONTAINER_DEST $HOST_DEST"
docker cp $container:$CONTAINER_DEST $HOST_DEST
if ! [ $? -eq 0 ] ; then
    echo "[KO] Unable to copy package, no such file or directory" >&2
    exit 1
fi

echo "[OK] Successfully copied package to $HOST_DEST"

docker rm ${container}
exit 0

#!/bin/bash

set -e

IMAGE_NAME="askme"
CONTAINER_NAME="askme"

docker build -t $IMAGE_NAME .

docker stop $CONTAINER_NAME 2> /dev/null || true
docker rm $CONTAINER_NAME 2> /dev/null || true

docker run -d --name $IMAGE_NAME -p 8000:8000 $CONTAINER_NAME

echo "Container started: http://127.0.0.1:8000"
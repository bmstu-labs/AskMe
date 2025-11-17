#!/bin/bash

set -e

IMAGE_NAME="askme"
CONTAINER_NAME="askme"
PORT=8000

while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

docker build -t $IMAGE_NAME .

docker stop $CONTAINER_NAME 2> /dev/null || true
docker rm $CONTAINER_NAME 2> /dev/null || true

docker run -d \
    --name $CONTAINER_NAME \
    -p ${PORT}:8000 \
    $IMAGE_NAME

echo "Container started: http://127.0.0.1:${PORT}"
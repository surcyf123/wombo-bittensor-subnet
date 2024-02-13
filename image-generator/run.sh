#!/bin/bash

set -e

docker build -f ../gpu-pipeline/Dockerfile -t wombo-subnet:gpu-pipeline ../
docker build -f Dockerfile -t wombo-subnet:image-generator ../

docker run \
  --network="host" \
  --gpus all \
  -v ~/.cache:/root/.cache \
  -v $(pwd)/cache:/app/image-generator/cache \
  -v $(pwd)/../checkpoints:/app/checkpoints \
  -it \
  --rm \
  wombo-subnet:image-generator \

#!/bin/bash

clear
docker container stop kafka
docker container remove kafka
docker build --no-cache  --tag kafka:1.0 .
docker run -p 8003:8003 \
    --name kafka \
    --network=mynet \
    -t kafka:1.0
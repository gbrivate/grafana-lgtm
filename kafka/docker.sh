#!/bin/bash
clear
docker container stop kafka
docker container remove kafka
docker build --no-cache  --tag kafka:1.0 .
docker run -d -p 8003:8003 -p 9102:9102 -p 9101:9101 \
    --name kafka \
    --network=mynet \
    -t kafka:1.0
#!/bin/bash

clear
docker container stop grafana
docker container remove grafana
docker image remove  lgtm:1.0
docker build --no-cache --tag lgtm:1.0 .
docker run -p 3000:3000 -p 4317:4317 -p 4318:4318 -p 4040:4040 -p 9090:9090  \
    --name grafana \
    --network=mynet \
    lgtm:1.0
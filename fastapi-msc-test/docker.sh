#!/bin/bash
# In case you wanna run only docker not on k8s
clear
docker container stop fastapi
docker container remove fastapi
docker build --no-cache  --tag fastapi-msc-test:latest .
docker run -d -p 8001:8001 \
    --name fastapi \
    --network=mynet \
    -t fastapi-msc-test:latest
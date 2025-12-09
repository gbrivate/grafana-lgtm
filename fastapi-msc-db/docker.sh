#!/bin/bash
clear
docker container stop fastapi-db
docker container remove fastapi-db
docker build --no-cache  --tag fastapi-msc-db:1.0 .
docker run -d -p 8002:8001 \
    --name fastapi-db \
    --network=mynet \
    -t fastapi-msc-db:1.0
#!/bin/bash
clear
docker container stop postgres
docker container remove postgres
docker build --no-cache -t postgres:1.0 .
docker run -d -p 5432:5432 \
    --name postgres \
    --network=mynet \
    -t postgres:1.0
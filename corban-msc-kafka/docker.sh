#!/bin/bash

clear
docker container stop fastapi-kafka
docker container remove fastapi-kafka
docker build --no-cache  --tag corban-msc-kafka:1.0 .
docker run -p 8004:8004 \
--name fastapi-kafka \
--network=mynet \
-t corban-msc-kafka:1.0
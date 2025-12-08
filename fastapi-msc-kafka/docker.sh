#!/bin/bash
clear
docker container stop fastapi-kafka
docker container remove fastapi-kafka
docker build --no-cache  --tag fastapi-msc-kafka:1.0 .
docker run -d -p 8004:8004 \
--name fastapi-kafka \
--network=mynet \
-t fastapi-msc-kafka:1.0
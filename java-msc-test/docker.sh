#!/bin/bash
clear
docker container stop java
docker container remove java
docker image remove java-msc-test:latest
docker build --no-cache  --tag java-msc-test:latest .
docker run -d -p 8080:8080 --name java --network=mynet -t java-msc-test:latest
#! /bin/bash

docker build -f consumer/Dockerfile -t consumer .
docker run --name consumer --network project-network --rm consumer
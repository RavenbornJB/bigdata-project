#! /bin/bash

docker build -f wiki-create-consumer/Dockerfile -t wiki-create-consumer .
docker run --name wiki-create-consumer --network project-network --rm wiki-create-consumer
#! /bin/bash

docker build -f wiki-create-producer/Dockerfile -t wiki-create-producer .
docker run --name wiki-create-producer --network project-network --rm wiki-create-producer
#! /bin/bash

docker build -f producer/Dockerfile -t producer .
docker run --name producer --network project-network --rm producer
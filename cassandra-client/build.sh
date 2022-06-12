#! /bin/bash

docker build -f cassandra-client/Dockerfile -t cassandra-client .
docker run --name cassandra-client --network project-network --rm cassandra-client
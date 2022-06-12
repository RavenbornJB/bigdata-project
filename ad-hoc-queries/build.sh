#! /bin/bash

docker build -f ad-hoc-server/Dockerfile -t ad-hoc-server .
docker run --name ad-hoc-server --network project-network -p 9042:9042 --rm ad-hoc-server
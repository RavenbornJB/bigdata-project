#! /bin/bash

docker build -f ad-hoc-queries/Dockerfile -t ad-hoc-server .
docker run --name ad-hoc-server --network project-network -p 5050:5050 --rm ad-hoc-server
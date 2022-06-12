#! /bin/bash

docker build -f precomputed-reports/Dockerfile -t reports-server .
docker run --name reports-server --network project-network -p 1729:1729 --rm reports-server
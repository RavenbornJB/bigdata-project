#! /bin/bash

echo 'Creating nodes.'
docker run --name cassandra-server --network project-network -d cassandra:latest
until docker exec cassandra-server cqlsh &> /dev/null
do
	sleep 1
done
echo 'Node 1 created.'

docker exec cassandra-server mkdir /opt/app
docker cp ddl.cql cassandra-server:/opt/app
docker exec cassandra-server cqlsh --file /opt/app/ddl.cql

echo 'DONE.'

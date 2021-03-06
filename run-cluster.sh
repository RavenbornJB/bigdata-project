#! /bin/bash

echo 'Running Kafka and Zookeeper'
docker network create project-network
docker run -d --name zookeeper-server --network project-network -e ALLOW_ANONYMOUS_LOGIN=yes bitnami/zookeeper:latest
docker run -d --name kafka-server --network project-network -e ALLOW_PLAINTEXT_LISTENER=yes -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181 bitnami/kafka:latest
echo 'Awaiting completion of server init'
sleep 10

# decided to create topic in the same script
docker run -it --rm --network project-network -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181 bitnami/kafka:latest kafka-topics.sh --create  --bootstrap-server kafka-server:9092 --replication-factor 1 --partitions 3 --topic wiki-create


echo 'Running Cassandra'
docker run --name cassandra-server --network project-network -d cassandra:latest
until docker exec cassandra-server cqlsh &> /dev/null
do
	sleep 1
done
echo 'Node 1 created.'

docker exec cassandra-server mkdir /opt/app
docker cp cassandra-client/create-tables.cql cassandra-server:/opt/app
docker exec cassandra-server cqlsh --file /opt/app/create-tables.cql

echo 'DONE.'

# Course project - Big Data Processing

## Team

- [Dmytro Lutchyn](https://github.com/dlutchyn)
- [Yarema Mishchenko](https://github.com/RavenbornJB)

## System design

Our system consists of 4 independent services, as well as Kafka, Zookeeper, and Cassandra instances.

These 4 services are, as named in the project:

- `producer/producer.py` - responsible for fetching the Wikipedia data from the stream and passing it forward
- `consumer/consumer.py` - responsible for processing the data, filling Cassandra tables and maintaining a Pandas dataframe
- `precomputed-reports/reports_server.py` - responsible for maintaining a JSON file with precomputed outputs and serving it upon request
- `ad-hoc-queries/ad_hoc_server.py` - responsible for maintaining a Cassandra client connection and serving query results upon request.

In the diagram below, you can see how all those components create a coherent system.

### Diagram

![diagram](project-results/screenshots/diagram.png)

### Kafka - producer & consumer

As events come into the system, they pass through a Kafka MQ. This is done for scalability as well as for separating services with different purposes. Preprocessing events in the producer allows the consumer to focus on the important logic, which is writing records to a Cassandra DB and precomputing reports.

For reports from Category A, we are using Pandas instead of Apache Spark. The reason is twofold:

- The amount of data is small enough to be suitable for a non-distributed system. We are keeping track of all records from the last 8 hours, which (at the rate of ~2/sec) there are about 57k. Given that one entry usually weighs no more than 500 bytes (pessimistic estimate, for long titles), we can easily fit our records in less than 30 MB.
- We are more comfortable with Pandas :D While often overlooked, the amount of developer's experience in a framework is often extremely important for a streamlined development process.

### Cassandra - DB for storage

Our Cassandra storage has 5 different tables for each ad-hoc queries. 

- domains -> `(domain text), PIRMARY KEY (domain)`
- page_user -> `(domain text, page_name text, user_id int, page_id int,) PRIMARY KEY (user_id, domain, page_id)`
- page_domains -> `(domain text, page_id int) PRIMARY KEY (domain, page_id)`
- pages_info -> `(page_id int, page_name text, domain text, created_at timestamp) PRIMARY KEY (page_id, domain)`
- page_users_info -> `(user_id int, username text, page_id int, created_at timestamp) PRIMARY KEY (user_id, created_at, page_id)`

This way the use of tables becomes easier and more efficient when doing SELECT queries. 

You can check out `cassandra-client/create-tables.cql` for keyspace initialization.

### Precomputed reports server - Category A

Every hour, the consumer recomputes records for the last 6 full hours, excluding the last hour. These requests, in a JSON form, are then sent via a POST request to our precomputed server. Here, the server stores `queries.json` to give out on a GET request, which you can do as a client via port forwarding.

### Ad hoc server - Category B

Consumer creates CassandraClient that updates all existing tables as soon as the new message comes to Kafka. CassandraClient has separate methods for inserting data to different tables (`insert_to_page_user`, etc.), and methods for getting answers to all queries (`select_from_pages_info`, etc.)

To get SELECT results we have separate script that gets requests from the server and executes corresponding SELECT queries.

`client_demo.py` sends these requests via POST request to the server.

## Results

All of our results are stored in the `project-results` directory. These results are generated using the `client_demo.py` script. As per the duration requirement, the system was running for ~8h 27m before making the requests.

### Category A

For category A, the JSON file with query results is saved to `project-results/queries.json`.

The file is extremely large because of the 3rd query: the top author created over 20000 pages.

First query:

![category A - 1st query](project-results/screenshots/category_a-1st.jpg)

Second query:

![category A - 2nd query](project-results/screenshots/category_a-2nd.jpg)

Third query:

![category A - 3rd query](project-results/screenshots/category_a-3rd.jpg)

### Category B

As for category B, the output is displayed directly when running `client_demo.py`.

The arguments were chosen to fit well in a screen.

![category B](project-results/screenshots/category_b.jpg)

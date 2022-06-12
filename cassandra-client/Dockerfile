FROM python:3.9-slim

RUN pip install --upgrade pip
RUN pip install cassandra-driver

COPY cassandra-client/cassandra_client.py /opt/app/
COPY cassandra-client/fill_tables.py /opt/app/

CMD ["python", "fill_tables.py"]

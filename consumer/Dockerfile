FROM python:3.9-slim
RUN pip install --upgrade pip
RUN pip install kafka-python cassandra-driver pandas

COPY wiki-create-consumer/consumer.py /opt/app/
COPY precomputed-reports/compute_reports.py /opt/app/
COPY cassandra-client/cassandra_client.py /opt/app/

ENTRYPOINT ["python", "/opt/app/consumer.py"]
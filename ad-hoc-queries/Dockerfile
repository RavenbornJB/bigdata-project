FROM python:3.9-slim
RUN pip install --upgrade pip
RUN pip install flask cassandra-driver

COPY ad-hoc-queries/ad-hoc-server.py /opt/app/
COPY cassandra-client/cassandra_client.py /opt/app/

ENTRYPOINT ["python", "/opt/app/ad-hoc-server.py"]
FROM python:3.9-slim
RUN pip install --upgrade pip
RUN pip install kafka-python sseclient

COPY wiki-create-producer/producer.py /opt/app/

ENTRYPOINT ["python", "/opt/app/producer.py"]
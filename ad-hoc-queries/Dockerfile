FROM python:3.9-slim
RUN pip install --upgrade pip
RUN pip install flask

COPY ad-hoc-server.py /opt/app/

ENTRYPOINT ["python", "/opt/app/ad-hoc-server.py"]
FROM python:3.9-slim
RUN pip install --upgrade pip
RUN pip install flask

COPY reports_server.py /opt/app/

ENTRYPOINT ["python", "/opt/app/reports_server.py"]
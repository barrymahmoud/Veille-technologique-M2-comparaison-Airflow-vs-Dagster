FROM python:3.12-slim
WORKDIR /opt/project/dagster
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV DAGSTER_HOME=/opt/dagster_home PROJECT_DIR=/opt/project
RUN mkdir -p /opt/dagster_home
CMD ["dagster", "dev", "-f", "/opt/project/dagster/definitions.py", "-h", "0.0.0.0", "-p", "3000"]

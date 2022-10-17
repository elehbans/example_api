FROM python:3.10
WORKDIR /api
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
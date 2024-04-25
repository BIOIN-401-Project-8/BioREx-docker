FROM nvcr.io/nvidia/tensorflow:24.02-tf2-py3

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

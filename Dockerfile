FROM tensorflow/tensorflow:2.9.3-gpu

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

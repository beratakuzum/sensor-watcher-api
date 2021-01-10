FROM python:3.7-slim
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD gunicorn run:app -b 0.0.0.0:8080
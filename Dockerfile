FROM python:3.7.3-slim
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python run.py
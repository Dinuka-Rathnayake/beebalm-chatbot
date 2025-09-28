# docker script for containerizing the app

# base image
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy the files
COPY requirements.txt requirements.txt
COPY .env .env

# install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY .env .
COPY requirements.txt .


EXPOSE 8001

CMD ["python", "app.py"]
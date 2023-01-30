FROM python:3.9-slim-buster

LABEL MAINTAINER="Cong Minh Tran <minhtc6@viettel.com.vn>"

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements, cv2 dependencies 
RUN apt-get update
RUN apt-get install -y --no-install-recommends libgl1 libglib2.0-0 dos2unix

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --default-timeout=900 --no-cache-dir -r requirements.txt

WORKDIR /backend
COPY . /backend

# During debugging, this entry point will be overridden.
RUN dos2unix ./entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
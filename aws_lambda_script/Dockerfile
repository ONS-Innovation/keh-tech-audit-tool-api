# Use an official Python runtime as a parent image
# FROM public.ecr.aws/lambda/python:3.12
FROM public.ecr.aws/docker/library/python:3.12-alpine3.22
# Install aws-lambda-cpp build dependencies
RUN apk add -no-cache \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev
# Set the working directory in the container
WORKDIR /var/task
# Upgrade pip tooling
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Install Lambda Runtime Interface Client
RUN pip install --no-cache-dir awslambdaric
# Create a non-root user and group manually
RUN mkdir -p /home/appuser && \
    chown -R 1000:1000 /home/appuser
# Copy the requirements.txt first to leverage Docker's cache for dependencies
COPY requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the app folder (with your Flask app) and the lambda_handler.py
COPY app/ /var/task/app/
COPY main.py /var/task/
# Change ownership of the application files to the non-root user
RUN chown -R 1000:1000 /var/task
# Switch to non-root user
USER 1000
# The CMD specifies the handler to use in AWS Lambda
CMD ["main.lambda_handler"]
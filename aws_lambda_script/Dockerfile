# # Use an official Python runtime as a parent image
# FROM public.ecr.aws/lambda/python:3.12
# # Set the working directory in the container
# WORKDIR /var/task
# # Upgrade tooling and awslambdaric
# RUN pip install --no-cache-dir --upgrade pip setuptools wheel awslambdaric 
# # && \ pip install --no-cache-dir --upgrade awslambdaric
# # Create a non-root user and group manually
# RUN mkdir -p /home/appuser && \
#     chown -R 1000:1000 /home/appuser
# # Copy the requirements.txt first to leverage Docker's cache for dependencies
# COPY requirements.txt .
# # Install the dependencies
# RUN pip install --no-cache-dir -r requirements.txt
# # Copy the app folder (with your Flask app) and the lambda_handler.py
# COPY app/ /var/task/app/
# COPY main.py /var/task/
# # Change ownership of the application files to the non-root user
# RUN chown -R 1000:1000 /var/task
# # Switch to non-root user
# USER 1000
# # The CMD specifies the handler to use in AWS Lambda
# CMD ["main.lambda_handler"]

FROM python:3.12-slim AS builder
WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN --mount=type=secret,id=github_token \
    set -e; \
    if [ -f /run/secrets/github_token ]; then \
      GITHUB_TOKEN="$(cat /run/secrets/github_token)"; \
      git config --global url."https://${GITHUB_TOKEN}:x-oauth-basic@github.com/".insteadOf "https://github.com/"; \
    fi; \
    pip install --no-cache-dir -r requirements.txt; \
    rm -f /root/.gitconfig 2>/dev/null || true
    
# RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime (Lambda base)
FROM public.ecr.aws/lambda/python:3.12
WORKDIR /var/task

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app/ /var/task/app/
COPY main.py /var/task/

# Change ownership of the application files to the non-root user
RUN chown -R 1000:1000 /var/task
# Switch to non-root user
USER 1000

CMD ["main.lambda_handler"]
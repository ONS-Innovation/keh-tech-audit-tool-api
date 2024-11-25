FROM public.ecr.aws/lambda/python:3.12

# Set the working directory in the container
WORKDIR /var/task

# Copy the requirements.txt first to leverage Docker's cache for dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app folder (with your Flask app) and the lambda_handler.py
COPY app/ /var/task/app/
COPY main.py /var/task/

ENV TECH_AUDIT_DATA_BUCKET=sdp-dev-tech-audit-tool-api-tool
ENV TECH_AUDIT_SECRET_MANAGER=sdp-dev-tech-audit-tool-api-cognito-secrets
ENV AWS_DEFAULT_REGION=eu-west-2
ENV AWS_COGNITO_TOKEN_URL=https://tech-audit-tool-api-sdp-dev.auth.eu-west-2.amazoncognito.com/oauth2/token


# The CMD specifies the handler to use in AWS Lambda
CMD ["main.lambda_handler"]
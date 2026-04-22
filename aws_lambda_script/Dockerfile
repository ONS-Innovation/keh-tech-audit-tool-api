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

# Stage 2: runtime (Lambda base)
FROM public.ecr.aws/lambda/python:3.12
WORKDIR /var/task

# Copy dependencies into /var/task so Lambda always imports them
COPY --from=builder /opt/venv/lib/python3.12/site-packages/ /var/task/

# Ensure /var/task is on sys.path
ENV PYTHONPATH="/var/task:${PYTHONPATH}"

COPY app/ /var/task/app/
COPY main.py /var/task/

# Change ownership of the application files to the non-root user
RUN chown -R 1000:1000 /var/task
# Switch to non-root user
USER 1000

CMD ["main.lambda_handler"]
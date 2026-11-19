FROM python:3.12-alpine@sha256:c5ba3deef00c7758561a0f03c26f44f10589263d40e732b8748e0d1f38f6dd89
# Deliberately omit OS upgrades to demonstrate failing the Trivy security gate in PR-only negative test
ENV PORT=8080 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY app/server.py /app/server.py
USER 10001:10001
EXPOSE 8080
CMD ["python", "-B", "/app/server.py"]

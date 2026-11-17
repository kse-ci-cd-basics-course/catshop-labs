FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -u 10001 -r appuser && mkdir -p /data && chown -R appuser:appuser /data
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser app.py .
USER appuser
EXPOSE 8080
CMD ["python", "app.py"]
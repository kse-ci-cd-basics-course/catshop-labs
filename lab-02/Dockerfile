FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --create-home app && mkdir /data && chown app:app /data
USER app

EXPOSE 8080
CMD ["python", "app.py"]
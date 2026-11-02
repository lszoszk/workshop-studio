FROM python:3.12-slim
LABEL app=studio-api
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py models.py seats.py ./
ENV STUDIO_STATE_DIR=/state STUDIO_DATA_DIR=/data STUDIO_SEATS_CSV=/state/seats.csv PYTHONUNBUFFERED=1
EXPOSE 8011
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8011/studio-api/health').status==200 else 1)"
# --no-access-log: uvicorn's access log would hold client addresses; the app logs its own content-free lines
CMD ["uvicorn", "--factory", "app:create_app", "--host", "0.0.0.0", "--port", "8011", "--workers", "1", \
     "--no-access-log", "--timeout-graceful-shutdown", "10"]

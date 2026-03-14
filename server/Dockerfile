FROM python:3.13

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

# load and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# load in all application files
COPY --chown=appuser:appuser app ./app
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# listening port
EXPOSE 80

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80"]
FROM python:3.13

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
COPY --chown=appuser:appuser . .

RUN pip install --no-cache-dir -r requirements.txt

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
FROM python:3.13

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app/ .

USER appuser

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
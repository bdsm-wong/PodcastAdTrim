FROM python:3.13

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

# load and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# load in all application files
COPY --chown=appuser:appuser . .
USER appuser

# listening port
EXPOSE 80

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:80"]
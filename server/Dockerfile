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

# create subdirectories in storage volume
RUN mkdir storage/test1
RUN mkdir storage/test2

# create log files
RUN touch test.log

# listening port
EXPOSE 80

# call gunicorn to serve the app
CMD gunicorn "app:app" \
    --workers ${GUNICORN_WORKERS} \
    --timeout ${GUNICORN_TIMEOUT} \
    --bind "0.0.0.0:80"

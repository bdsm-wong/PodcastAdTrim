FROM python:3.13

# create system user for added security
RUN adduser --system nonroot
USER nonroot
WORKDIR /home/nonroot
WORKDIR /app

# copy all the files to the container
COPY . .

# venv
ENV VIRTUAL_ENV=/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=main.py
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 8090

CMD ["python", "main.py"]
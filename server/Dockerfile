FROM ubuntu:latest

# upgrade pip
RUN python -m pip install --upgrade pip

# create system user for added security
RUN adduser --system nonroot
USER nonroot
WORKDIR /home/nonroot

# copy all the files to the container
COPY . .

# venv
ENV VIRTUAL_ENV=/home/nonroot/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=main.py
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 8090

CMD ["python", "main.py"]
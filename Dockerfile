# base image
FROM python:3.10-slim
# setup environment variable
ENV DockerHOME=/aiogram-django


# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./aiogram-django/requirements.txt $DockerHOME
# run this command to install all dependencies
RUN pip install -r requirements.txt

COPY ./aiogram-django/requirements-dev.txt $DockerHOME
RUN pip install -r requirements-dev.txt

COPY ./aiogram-django $DockerHOME

#RUN ["apt-get", "update"]
#RUN ["apt-get", "-y", "install", "vim"]

RUN apt update
RUN apt install make

# port where the Django app runs
EXPOSE 8080
# start server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
#CMD ["make", "-j3", "run-local-server"]
#CMD ["python", "-m", "app.delivery.bot"]
CMD ["make", "-j3", "run-local-server", "run-bot"]

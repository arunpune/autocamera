# syntax=docker/dockerfile:1
# For more information, please refer to https://aka.ms/vscode-docker-python

FROM python:3.8-slim-buster

EXPOSE 5000
#ENV buildTag=1.0
ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#WORKDIR /app
WORKDIR /autocameratest2


RUN apt-get update \
    && apt-get -y install --reinstall build-essential \
    && apt-get install -y gcc python-opencv 


# Install pip requirements
COPY requirements.txt requirements.txt

#RUN pip3 install -r requirements.txt
RUN pip install --no-cache-dir wheel \
    && pip install --no-cache-dir -r requirements.txt


COPY . .


#CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "\autocameratest2\src\app:app"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
#CMD ["flask", "run", "--host=0.0.0.0"]

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#/app changed to /src
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#uncomment below
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /src
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "autocameratest2\src\app:app"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "python3", "-m" , "flask", "run", "autocameratest2\src\app:app"]


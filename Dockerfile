FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN apt update -y
RUN apt install build-essential -y
RUN pip install -r requirements.txt
RUN apt-get purge --auto-remove build-essential -y

# Bundle app source
COPY src /app

CMD [ "python", "src/main.py" ]


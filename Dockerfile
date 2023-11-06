FROM python:3.11-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN apk add gcc
RUN pip install -r requirements.txt
RUN apk remove gcc

# Bundle app source
COPY src /app

CMD [ "python", "src/main.py" ]


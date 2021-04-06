# Merval-Realtime-API

Simple RESTful server for realtime merval data.

## How to setup

Include config.json file that has the following format:

{
"dni": "XXXXXXX",
"user": "XXXXXXXx",
"password": "XXXXXXX",
"broker_id": 12
}

Refer to https://github.com/crapher/pyhomebroker for broker_id and other setup information.

## Build with docker

docker build -t merval-server .

## Run with docker

docker run -d --name merval-realime-api -p 8000:8000 merval-server

## Visit 127.0.0.1:8000/docs to try it out!

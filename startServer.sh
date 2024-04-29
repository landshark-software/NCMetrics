#!/bin/bash

export X_FOR_HEADERS=2
export X_PROTO_HEADERS=2
export X_HOST_HEADERS=1
export X_PREFIX_HEADERS=1

nohup gunicorn -w 2 --certfile=../ssl/cert.pem --keyfile=../ssl/key.pem -b 127.0.0.1:8000 'Server:app' &
export SERVER_PID=$!

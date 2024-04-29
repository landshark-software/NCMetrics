#!/bin/bash

sudo sed -i "/#\$nrconf{restart} = 'i';/s/.*/\$nrconf{restart} = 'a';/" /etc/needrestart/needrestart.conf
sudo sed -i "s/#\$nrconf{kernelhints} = -1;/\$nrconf{kernelhints} = -1;/g" /etc/needrestart/needrestart.conf
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip -y
sudo apt install awscli -y

sudo apt install nginx -y
sudo apt install gunicorn -y
pip install Flask
pip install Flask-Limiter
pip install requests
pip install boto3
pip install mcstatus

mkdir ~/ssl
openssl req -x509 -newkey rsa:4096 -keyout ~/ssl/key.pem -out ~/ssl/cert.pem -sha256 -days 3650 -nodes -subj '/CN=localhost'

sudo aws s3 cp s3://nc-metrics-service-config/default /etc/nginx/sites-enabled/default
sudo aws s3 cp s3://nc-metrics-service-config/CFCert.crt /etc/ssl/certs/CFCert.crt
sudo aws s3 cp s3://nc-metrics-service-config/CFKey.key /etc/ssl/private/CFKey.key

sudo nginx

export X_FOR_HEADERS=2
export X_PROTO_HEADERS=2
export X_HOST_HEADERS=1
export X_PREFIX_HEADERS=1

nohup gunicorn -w 2 --certfile=../ssl/cert.pem --keyfile=../ssl/key.pem -b 127.0.0.1:8000 'Server:app' &
export SERVER_PID=$!

echo "*/5 * * * * python3 /home/ubuntu/NCMetrics/MetricsCollector.py" | crontab

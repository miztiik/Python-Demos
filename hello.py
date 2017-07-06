#!/usr/bin/python
# -*- coding: utf-8 -*-

# import boto3
# 
# 
# ec2 = boto3.resource('ec2')
# vpc = ec2.Vpc('id')
# 
# 
# yum -y install epel-release
# yum -y install python-pip unzip
# pip install --upgrade pip
# pip install requests unidecode flask flask-ask
# cd /tmp;curl -O https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip


import feedparser, json, time , traceback

from datetime import datetime
from flask import Flask
from flask import request


app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to my world"



if __name__ == "__main__":
    app.run()





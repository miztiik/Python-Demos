##################################################################################
## 
## VERSION      :   0.0.1
## DATE         :   10Jan2017
##                              
## USAGE        :   Dockerfile to build a super lightweight container to run media metadata fetcher from OMDB, IMDB & TVDB
##################################################################################

FROM python:alpine
MAINTAINER Mystique
RUN pip install request requests flask
RUN mkdir -p /var/app

# Copy application code from host to container image
COPY . /var/app/

# Expose external connectivity port & the web interface
EXPOSE 5000

# Setting up the entry point to allow for graceful exit when the container is stopped
# ENTRYPOINT [ "python", "/var/app/app.py" ]
# CMD [ "&" ]
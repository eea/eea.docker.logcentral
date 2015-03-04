Docker-based centarlized logging app

## Setting up

* Install docker 
* Install docker-compose
* Build the images ```docker-compose build```
* Start the app ```docker-compose up```

## Structure

* fluentd: A fluentd _log collector_ instance listening for syslog messages
* elasticsearch: An elasticsearch instance in which logs are _stored_ to be
  searched
* web: A nginx instance exposing the web interfaces used to _analyze_ logs

* generators(for demo purposes): python applications sending syslog messages for testing


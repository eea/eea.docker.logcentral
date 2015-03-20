Docker-based centarlized logging app

## Setting up

* Install docker 
* Install docker-compose
* Start the app ```docker-compose up```

## Structure

* fluentd: A fluentd _log collector_ instance listening for syslog messages
* web: A nginx instance exposing the web interfaces used to _analyze_ logs
* graylog: A graylog2 instance used for _storing_ and _analyzing_ logs

* demo/ a set of scripts to generate logs to be collected by the system 
  defined in this repo

## Interface
To access log analysis tools we you can go to:
* http://localhost/ for a graylog2 interface

## Testing that it works

* ```docker-compose up```
* ```cd demo/```
* ```./gen_syslog.py```

## Testing traceback logging

To log full tracebacks applications have to be set to use a GELFHandler.
An example of such application can be found in:
```./demo/gen_gelf_tracebacks.py```

Note: These tracebacks will only be viewable in the graylog2 interface

* ```cd demo```
* If running for the first time
  * ```virtualenv sandbox```
  * ```source sandbox/bin/activate
  * ```pip install -r requirements.txt
* ```./gen_gelf_tracebacks.py```

## Ports forwarded on the local machine

* 8000 - the web interface on the nginx server
* 5140 - the Syslog UDP port listening for syslog messages
* 12201 - the GELF port listening for GELF messages

## Development tips

If you want to modify something in the base image follow these steps:
* Pull eea.docker.graylog2 https://github.com/eea/eea.docker.graylog2
* Pull eea.docker.fluentd https://github.com/eea/eea.docker.fluentd
* Change the ```image: eeacms/graylog2``` or ```image: eeacms/fluentd``` to
  ```build: /path/to/eea.docker.graylog2``` or ```build:
  /path/to/eea.docker.fluentd```
* Remove existing images ```docker-compose rm```
* Build the images from the local repo ```docker-compose build```
* Start the services ```docker-compose up```

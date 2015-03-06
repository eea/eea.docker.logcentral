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

* demo/ a set of scripts to generate logs to be collected by the system 
  defined in this repo

## Interface
To access log analysis tools we you can go to:
* http://localhost:8000/ for a graylog2 interface
* http://localhost:8000/kibana for a kibana interface

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

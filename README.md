Docker-based centarlized logging app

## Setting up

Pre-requisites: install docker and docker-compose.

```
# git clone https://github.com/eea/eea.docker.logcentral.git
# cd eea.docker.logcentral
# cp .dummy-secret.env .secret.env
```
Configure the password (one time only) and start up the graylog2 app

```
# vi .secret.env
# docker-compose up -d
```

Verify that the app is running by doing ```docker-compose ps```

Now you can access the graylog2 web interface on port 80 (default):
* http://localhost/

## Structure

* fluentd: A fluentd _log collector_ instance listening for syslog messages
* web: A nginx instance exposing the web interfaces used to _analyze_ logs
* graylog: A graylog2 instance used for _storing_ and _analyzing_ logs

* demo/ a set of scripts to generate logs to be collected by the system 
  defined in this repo


## Testing that it works

* ```docker-compose up```
* ```cd demo/```
* ```./gen_syslog.py```

## Testing traceback logging

To log full tracebacks applications have to be set to use a GELFHandler.
An example of such application can be found in:

```
./demo/gen_gelf_tracebacks.py
```

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
* Build the images from the local repo ```docker-compose build```
* Start the services ```docker-compose up```

## Handling data and updates

__NOTE:__ Do not run ```docker-compose rm``` unless you __know__ what you
are doing. This will drop the data volume containing the settings and the
stored logs.

Correct update procedure should follow these steps:
* If the services in docker-compose changed, create a copy of the
  docker-compose file: cp docker-compose.yml docker-compose-old.yml
* Get the latest config from git ```git pull origin master```
* Pull the latest builds for the given tags: ```docker-compose pull```
* Stop the services defined in the old docker-compose file:
  ```docker-compose -f docker-compose-old.yml stop```
* Optionally backup your data using something similar with
  ```docker run --volumes-from eeadockerlogcentral_data_1 someimage $BACKUP_COMMAND``` 
* Start the freshly pulled services: ```docker-compose up```
* Remove the backup docker-compose file: ```rm docker-compose-old.yml```

__Note:__ The copy is needed as services can be renamed or removed during
the git pull, making ```docker-compose stop``` ignore the other running
services.

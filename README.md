# Docker-based centralized logging app based on Graylog2

## Setting up

Pre-requisites: install docker and docker-compose.

```
# git clone https://github.com/eea/eea.docker.logcentral.git
# cd eea.docker.logcentral
# cp .dummy-secret.env .secret.env
```
Configure the passwords (one time only) and start up the graylog2 app

```
# Configure Graylog password
# vi .secret.env
# Configure Broker authentication credentials
# vi .secret.rabbitmq
# Start Graylog2 app
# docker-compose up -d
```

Verify that the app is running by doing ```docker-compose ps```

Now you can access the graylog2 web interface on port 80 (default):
* http://localhost/
 
## How to upgrade

```
# docker-compose stop
# docker-compose pull
# docker-compose rm -v fluentd graylog rabbitmq rabbitmqconfig web
# docker-compose up -d --x-smart-recreate
```

## How to enable LDAP security
```
# Go to System > Users > Configure LDAP
* LDAP Server Address - ldap2.eionet.europa.eu : 389 : StartTLS # NOTE! use the nearest ldap, e.g. ldap4.eionet.europa.eu if you deploy on the cloud.
* Search Base DN - ou=Users,o=EIONET,l=Europe
* User Search Pattern - (&(objectClass=inetOrgPerson)(uid={0}))
* Display Name attribute - cn
* Default permission group - Reader
```

## How to set user the time zone

Since Graylog internally processes and stores messages in the UTC timezone, it is important to set the correct timezone for each user.

Even though the system defaults are often enough to display correct times, in case your team is spread across different timezones, each user can be assigned and change their respective timezone setting. You can find the current timezone settings for the various components on the System -> Overview page of your Graylog web interface.

To change your Timezone, go to System -> Users and edit the user's preferences

## How to add a new GELF AMQP input

```
# Go to System > Input > GELF AMQP > Launch new input
* Check global input
* title - your chioice e.g. "GELF AMQP"
* queue - log-messages (mandatory)
* username - USER from .secret.rabbitmq
* prefetch count - leave the default
* broker hostname - rabbitmq (name of the service in docker-compose.yml)
* broker virtualhost - / (encoded as "%2F" in the test script)
* broker port 5672
* password - PASS from .secret.rabbitmq
* ... defaults
* exchange - logging.gelf (mandatory)
```

Now you can log in RabbitMQ. Example URI:
```
amqp://{user}:{password}@{host}:5672/%2F (for user and password use values from .secret.rabbitmq)
```
If logging does not work just do a ```docker-compose run --rm rabbitmqconfig``` It will recreate the rabbitmq config so things get logged


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

## Common issues

__Problem:__ After graylog container is restart it will stop and restart over and over again.

__Fix:__ Enter graylog container and delete /opt/graylog2-web-interface/RUNNING_PID file

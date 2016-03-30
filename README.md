# Docker-based centralized logging app based on Graylog2

### Prerequisites

- Install [Docker](https://docs.docker.com/installation/)
- Install [Compose](https://docs.docker.com/compose/install/)

## Setting up

Pre-requisites: install docker and docker-compose.

Clone the repository

```
git clone https://github.com/eea/eea.docker.logcentral.git
cd eea.docker.logcentral
cp .dummy-secret.env .secret.env
cp .postfix.secret.example .postfix.secret
```
Configure the passwords (one time only) and start up the graylog2 app

```
# Configure Graylog password
vi .secret.env
# edit email configuration
vi .postfix.secret
# edit graylog email transport configuration
vi graylog.env
```

Choose the docker compose to run

* docker-compose.singlenode.yml: to start graylog with a single node
* docker-compose.multinode.yml: to start graylog with more nodes

```
# make a link of choosed docker-compose
ln -sf <docker-compose choosed> docker-compose.yml
# Start Graylog2 app
docker-compose up -d
```

Verify that the app is running by doing ```docker-compose ps```

Now you can access the graylog2 web interface on port 80 (default):
* http://localhost/
 
## How to upgrade

```
docker-compose stop
docker-compose pull
docker-compose up -d 
```
## How to add another node

To add another node follow the below steps.

__1__. Edit the "docker-compose.multinode.yml" file and add another slave node coping this code:

```
graylog-client-<progressive number>:
    restart: always
    image: docker.io/eeacms/graylog2:<latest tag>
    hostname: graylogclient<progressive number>.service
    env_file:
        - .secret.env
        - graylog.env
    environment:
        - ENABLED_SERVICES=graylog-server
        - GRAYLOG_MASTER=false
        - GRAYLOG_HOSTNAME=graylogclient<progressive_number>
    links:
        - "elasticsearch:elasticsearch.service"
        - "mongodb:mongodb.service"
        - "postfix:postfix.service"
    volumes_from:
        - data
    volumes:
        - ./config/graylogctl:/opt/graylog2-server/bin/graylogctl:z
        - /etc/localtime:/etc/localtime:ro
```
 
__2__. Register the new stack into ```GRAYLOG_SERVER_URIS``` of [graylog-web](docker-compose.multinode.yml#L88):

```
GRAYLOG_SERVER_URIS=http://graylogmaster:12900/,http://graylogclient:12900/,http://graylogclient<progressive_number>:12900/
```

__3__. Add the new node into load balancer

[udp](config/nginx.balancer.conf#L#L8-L11) load balancer configuration
```
upstream graylogserversudp {
    server graylogmaster:12201;
    server graylogclient:12201;
    server graylogclient<progressive_number>:12201;
}
```
[tcp](config/nginx.balancer.conf#L#L18-L21) load balancer configuration
```
upstream graylogserverstcp {
    server graylogmaster:1514;
    server graylogclient:1514;
    server graylogclient<progressive_number>:1514;
}
```

__4__. After you can stop and restart services

```
docker-compose stop
docker-compose up -d
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

## How to add a new GELF UDP input

```
# Go to System > Input > GELF UDP > Launch new input
* Check global input
* title - your chioice e.g. "GELF UDP"
* bind address - leave the default
* port - 12201
* receive buffer size - leave the default

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

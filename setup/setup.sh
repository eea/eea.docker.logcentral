#!/bin/sh

mkdir -p /data/elasticsearch /logs/elasticsearch
mkdir -p /data/mongodb /logs/mongodb

chmod -R 755 /data /logs && \
    chown -R 105:100 /data/elasticsearch /logs/elasticsearch && \
    chown -R 999:999 /data/mongodb /logs/mongodb

sed -i -e "s/password_secret =.*$/password_secret = $(pwgen -s 96)/" /etc/graylog/server/server.conf

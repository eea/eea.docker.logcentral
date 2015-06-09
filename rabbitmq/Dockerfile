FROM rabbitmq:3-management

RUN HOME=/var/lib/rabbitmq
CMD echo "[{rabbit, [\
             {loopback_users, []},\
             {default_user, <<\"$USER\">>},\
             {default_pass, <<\"$PASS\">>}]}]." > /etc/rabbitmq/rabbitmq.config && rabbitmq-server

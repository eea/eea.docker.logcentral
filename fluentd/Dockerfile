FROM kiyoto/fluentd:0.10.56-2.1.1
RUN mkdir /etc/fluent
RUN mkdir /log
ADD fluent.conf /etc/fluent/
RUN /usr/local/bin/gem install fluent-plugin-record-reformer --no-rdoc --no-ri
RUN /usr/local/bin/gem install fluent-plugin-elasticsearch --no-rdoc --no-ri
RUN /usr/local/bin/gem install gelf --no-rdoc --no-ri
RUN mkdir /etc/fluent/plugin
ADD out_gelf.rb /etc/fluent/plugin/
ENTRYPOINT /usr/local/bin/fluentd -c /etc/fluent/fluent.conf

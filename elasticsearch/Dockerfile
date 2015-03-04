FROM dockerfile/elasticsearch
RUN mkdir /conf
RUN mkdir /plugins
COPY ./elasticsearch.yml /conf/
COPY ./logging.yml /conf/
RUN /elasticsearch/bin/plugin -Des.config=/conf/elasticsearch.yml --install mobz/elasticsearch-head
CMD /elasticsearch/bin/elasticsearch -Des.config=/conf/elasticsearch.yml


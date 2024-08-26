from ioc.anotations.beans.component import Component
from ioc.kafka.kafka_conf import KafkaConf
from ioc.kafka.topics.new_topic import Topic


@Component()
class TOPIC(Topic):

    def __init__(self, conf: KafkaConf):
        super().__init__(conf, "TOPIC")


@Component()
class AuditTopic(Topic):

    def __init__(self, conf: KafkaConf):
        super().__init__(conf, "audit")

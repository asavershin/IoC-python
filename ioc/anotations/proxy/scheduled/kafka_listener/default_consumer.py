from typing import Optional

from kafka import KafkaConsumer

from ioc.anotations.proxy.scheduled.scheduled import Scheduled
from ioc.kafka.consumers.consumer import Consumer
from ioc.kafka.consumers.consumer_record import ConsumerRecord
from ioc.kafka.kafka_conf import KafkaConf


class DefaultScheduledConsumer(Consumer, Scheduled):

    def __init__(self, conf: KafkaConf, obj, method, topic: str, group_id=str) -> None:
        self._consumer: KafkaConsumer = KafkaConsumer(
            topic,
            bootstrap_servers=conf.get_kafka_bootstrap_servers(),
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda m: m.decode('utf-8'),
            key_deserializer=lambda m: m.decode('utf-8'),
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='PLAIN',
            sasl_plain_username=conf.get_kafka_user(),
            sasl_plain_password=conf.get_kafka_password()
        )
        self._obj = obj
        self._method = method

    def schedule(self):
        record = self.consume()
        if record is not None:
            self._method(self._obj, self.consume())

    def consume(self) -> Optional[ConsumerRecord]:
        for message in self._consumer:
            record = ConsumerRecord(
                key=message.key,
                value=message.value
            )
            return record

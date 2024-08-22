from ioc.anotations.beans.component import Component
from ioc.kafka.producer import Producer


@Component()
class DefaultProducer(Producer):
    def produce(self, topic, key, value):
        print(f"Produce {key}, {value} to {topic}")

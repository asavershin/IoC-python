class KafkaListener:
    def __init__(self, group_id, topic):
        self._group_id = group_id
        self._topic = topic

    def __call__(self, method):
        # Помечаем метод как Kafka listener
        method._is_kafka_listener = True
        method.group_id = self._group_id
        method.topic = self._topic
        return method

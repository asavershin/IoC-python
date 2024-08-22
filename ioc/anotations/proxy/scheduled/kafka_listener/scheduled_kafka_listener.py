from ioc.anotations.proxy.scheduled.scheduled import Scheduled
from ioc.common_logger import log


class ScheduledKafkaListener(Scheduled):
    def __init__(self, obj, method, group_id, topic_name):
        self._obj = obj
        self._method = method
        self._group_id = group_id
        self._topic_name = topic_name

    def schedule(self):
        log.info(f"Scheduling Kafka listener for {self._topic_name} with groupId {self._group_id}")
        return self._method(self._obj, "TIFF")

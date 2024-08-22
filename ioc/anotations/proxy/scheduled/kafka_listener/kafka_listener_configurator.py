import inspect
import sys

from ioc.anotations.proxy.proxy_configurator import ProxyConfigurator
from ioc.anotations.proxy.scheduled.kafka_listener.scheduled_kafka_listener import ScheduledKafkaListener


class KafkaListenerProxyConfigurator(ProxyConfigurator):
    def get_my_order(self) -> int:
        return sys.maxsize

    def configure_if_needed(self, obj, application_context):
        obj_class = obj.__class__

        methods = inspect.getmembers(obj_class, predicate=inspect.isfunction)
        kafka_listener_methods = [
            (method_name, method) for method_name, method in methods
            if getattr(method, "_is_kafka_listener", False)
        ]

        if not kafka_listener_methods:
            return obj

        for method_name, method in kafka_listener_methods:
            # Создаём объект ScheduledKafkaListener вместо добавления метода schedule в класс
            scheduled_bean = ScheduledKafkaListener(
                obj=obj,
                method=method,
                group_id=method.group_id,
                topic_name=method.topic
            )
            # Передаем объект в контекст или где он должен быть использован
            application_context.add_scheduled_bean(scheduled_bean)

        return obj

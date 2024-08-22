import functools
import inspect
import sys

from ioc.anotations.proxy.proxy_configurator import ProxyConfigurator
from ioc.common_logger import log
from ioc.kafka.producer import Producer


class AuditProxyConfigurator(ProxyConfigurator):
    def get_my_order(self) -> int:
        return sys.maxsize - 100

    def configure_if_needed(self, obj, application_context):
        # Получаем класс объекта
        obj_class = obj.__class__

        methods = inspect.getmembers(obj_class, predicate=inspect.isfunction)
        has_audit_methods = any(getattr(method, "_is_audit", False) for _, method in methods)

        if not has_audit_methods:
            return obj
        for method_name, method in methods:
            if getattr(method, "_is_audit", False):
                # Создаём обёртку для метода
                wrapped_method = self.create_audit_wrapper(method_name, method, application_context)
                setattr(obj_class, method_name, wrapped_method)

        return obj

    def create_audit_wrapper(self, method_name, method, application_context):
        """Функция для создания обёртки с аудитом"""

        producer: Producer = application_context.get_bean(Producer)

        @functools.wraps(method)
        def wrapped(self, *args, **kwargs):
            class_name = self.__class__.__name__
            log.info(f"Audit start: {class_name}.{method_name} with arguments: {args} {kwargs}")
            result = method(self, *args, **kwargs)
            producer.produce("audit", "TIFF", "VALUE")
            return result

        return wrapped

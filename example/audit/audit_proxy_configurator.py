import functools
import inspect
import json
import sys
from typing import Any

from example.models.audit_entity import AuditEntity
from example.models.audit_with_result import AuditEntityWithResult
from example.models.error_audit import ErrorAudit
from example.models.fatal_audit import FatalAudit
from ioc.anotations.proxy.proxy_configurator import ProxyConfigurator
from ioc.kafka.producers.producer import Producer


class AuditProxyConfigurator(ProxyConfigurator):
    def get_my_order(self) -> int:
        return sys.maxsize - 100

    def configure_if_needed(self, obj, application_context):
        obj_class = obj.__class__

        methods = inspect.getmembers(obj_class, predicate=inspect.isfunction)
        has_audit_methods = any(getattr(method, "_is_audit", False) for _, method in methods)

        if not has_audit_methods:
            return obj
        for method_name, method in methods:
            if getattr(method, "_is_audit", False):
                wrapped_method = self.create_audit_wrapper(method_name, method, application_context)
                setattr(obj_class, method_name, wrapped_method)

        return obj

    def create_audit_wrapper(self, method_name, method, application_context):

        producer: Producer = application_context.get_bean(Producer)
        audit_topic = method.audit_topic
        success = "SUCCESS"
        error = "ERROR"

        @functools.wraps(method)
        def wrapped(self, *args, **kwargs):
            system = "exampleSystem"

            try:
                result = method(self, *args, **kwargs)

                if result is None:
                    _convert_and_produce(audit_topic, success, AuditEntity(system, self.__class__, method_name, args),
                                         producer)
                else:
                    with_result = AuditEntityWithResult(system, self.__class__, method_name, args, str(result))
                    _convert_and_produce(audit_topic, success, with_result, producer)

                return result

            except Exception as e:
                try:
                    error_audit = ErrorAudit(system, self.__class__, method_name, args, e.__class__, str(e))
                    _convert_and_produce(audit_topic, error, error_audit, producer)
                except Exception as e:
                    _convert_and_produce(audit_topic, error, FatalAudit(system, e.__class__, str(e)), producer)
                    raise e
                raise e

        return wrapped


def _convert_and_produce(topic: str, status: str, to_json: Any, producer: Producer):
    producer.produce(topic, status, json.dumps(to_json.__dict__))

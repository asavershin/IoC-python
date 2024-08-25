import os
from abc import ABC, abstractmethod

from ioc.anotations.beans.component import Component
from ioc.common_logger import log


class KafkaConf(ABC):
    @abstractmethod
    def get_kafka_user(self) -> str:
        pass

    @abstractmethod
    def get_kafka_password(self) -> str:
        pass

    @abstractmethod
    def get_kafka_bootstrap_servers(self) -> str:
        pass


@Component()
class DefaultKafkaConf(KafkaConf):
    def __init__(self):
        self._KAFKA_USER = os.getenv('kafka.user')
        self._KAFKA_PASSWORD = os.getenv('kafka.password')
        self._KAFKA_BOOTSTRAP_SERVERS = os.getenv('kafka.bootstrap-servers')
        log.info(f"DefaultKafkaConf start with {self._KAFKA_USER}|{self._KAFKA_PASSWORD}|{self._KAFKA_BOOTSTRAP_SERVERS}")

    def get_kafka_user(self) -> str:
        return self._KAFKA_USER

    def get_kafka_password(self) -> str:
        return self._KAFKA_PASSWORD

    def get_kafka_bootstrap_servers(self) -> str:
        return self._KAFKA_BOOTSTRAP_SERVERS

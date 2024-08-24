import logging
from abc import abstractmethod
from typing import Dict

from example.audit.audit import Audit
from ioc.anotations.beans.component import Component
from ioc.anotations.proxy.log.log import Log
from ioc.anotations.proxy.scheduled.kafka_listener.kafka_listener import KafkaListener
from ioc.kafka.consumers.consumer_record import ConsumerRecord

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Worker:
    @abstractmethod
    def process(self, message):
        pass

    @abstractmethod
    def get_my_key(self) -> str:
        pass


class Listener:
    @abstractmethod
    def listen(self, message: ConsumerRecord):
        pass


@Component()
class NdviTiffWorker(Worker):

    def process(self, message):
        print(f"{self.get_my_key()} process {message}")

    def get_my_key(self) -> str:
        return "TIFF"


@Component()
class NdviBillWorker(Worker):

    def process(self, message):
        print(f"{self.get_my_key()} process {message}")

    def get_my_key(self) -> str:
        return "BILL"


@Component()
class NdviListener(Listener):

    def __init__(self, workers: list[Worker]) -> None:
        self.workers: Dict[str, Worker] = {worker.get_my_key(): worker for worker in workers}

    @Audit("audit")
    @Log()
    @KafkaListener("group", "TOPIC")
    def listen(self, message: ConsumerRecord):
        self.workers.get(message.get_key()).process(message.get_value())

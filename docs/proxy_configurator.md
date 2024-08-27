# Проксирование 
На этапе bootstrap библиотека ищет классы унаследованные от [ProxyConfigurator](../ioc/anotations/proxy/proxy_configurator.py).
Все конфигураторы участвуют в настройке компонентов, проксируя их методы. Каждому конфигуратору соответствует один декоратор.

Конфигураторы по умолчанию:
1) [KafkaListenerProxyConfigurator](./proxyConfigurators/kafka_listener.md)
2) [LogProxyConfigurator](./proxyConfigurators/log.md)

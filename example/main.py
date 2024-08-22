import inspect

from example.services.components import Listener
from ioc.application_context import ApplicationContext
from ioc.common_logger import log

if __name__ == '__main__':
    context = ApplicationContext(["example.services"])
    context.run()
    print(context._cache)

    obj = context.get_bean(Listener)
    methods_after_config = inspect.getmembers(obj, predicate=inspect.ismethod)
    # for name, method in methods_after_config:
    #     print(f"{name}: {method}")
    while True:
        log.info("Try schedule")
        context.get_scheduled_beans()[0].schedule()

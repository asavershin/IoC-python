import inspect

from example.services.components import Listener
from ioc.application_context import ApplicationContext

if __name__ == '__main__':
    context = ApplicationContext(["example.services"])
    context.run()
    print("<<<<<<<<<<<<>>>>>>>>>>>>")
    print(context._cache)

    print("Methods after configuration:")
    obj = context.get_bean(Listener)
    methods_after_config = inspect.getmembers(obj, predicate=inspect.ismethod)
    for name, method in methods_after_config:
        print(f"{name}: {method}")
    print(obj.listen("TIFF"))
    print(context.get_scheduled_beans()[0].schedule())

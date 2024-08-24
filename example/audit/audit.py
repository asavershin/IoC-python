class Audit:
    def __init__(self, audit_topic):
        self._audit_topic = audit_topic

    def __call__(self, method):
        method._is_audit = True
        method.audit_topic = self._audit_topic
        return method

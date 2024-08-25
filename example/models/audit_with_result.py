from example.models.audit_entity import AuditEntity


class AuditEntityWithResult(AuditEntity):
    result: str

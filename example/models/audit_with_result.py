from dataclasses import dataclass

from example.models.audit_entity import AuditEntity


@dataclass(frozen=True)
class AuditEntityWithResult(AuditEntity):
    result: str

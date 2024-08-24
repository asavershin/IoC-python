from dataclasses import dataclass
from typing import Type

from example.models.audit_entity import AuditEntity


@dataclass(frozen=True)
class ErrorAudit(AuditEntity):
    cause: Type[BaseException]
    exceptionMessage: str

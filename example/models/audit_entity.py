from dataclasses import dataclass
from typing import Type, Any


@dataclass(frozen=True)
class AuditEntity:
    system: str
    activeClass: Type[Any]
    activeMethod: str
    params: tuple[Any, ...]

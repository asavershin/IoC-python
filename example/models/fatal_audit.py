from dataclasses import dataclass
from typing import Type


@dataclass(frozen=True)
class FatalAudit:
    system: str
    cause: Type[BaseException]
    exceptionMessage: str

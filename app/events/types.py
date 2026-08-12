from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class DomainEvent:
    event_type: str
    aggregate_id: str
    payload: dict[str, Any]
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

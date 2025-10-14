from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import Optional, Dict, Any

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    done: bool = False
    due: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["created_at"] = self.created_at.isoformat()
        d["due"] = self.due.isoformat() if self.due else None
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Task":
        due = date.fromisoformat(d["due"]) if d.get("due") else None
        created = datetime.fromisoformat(d["created_at"]) if d.get("created_at") else datetime.utcnow()
        return cls(
            id=int(d["id"]),
            title=str(d["title"]),
            description=str(d.get("description", "")),
            done=bool(d.get("done", False)),
            due=due,
            created_at=created,
        )

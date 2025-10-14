from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import date

from model.task import Task

class TaskController:
    def __init__(self, db_path: Path | str = "db.json") -> None:
        self.db_path = Path(db_path)
        self.db_path.touch(exist_ok=True)
        tasks = self._load()
        self._tasks: Dict[int, Task] = {t.id: t for t in tasks}
        self._next_id = max(self._tasks.keys(), default=0) + 1

    # --- persistance ---
    def _load(self) -> List[Task]:
        raw = self.db_path.read_text(encoding="utf-8") or "[]"
        return [Task.from_dict(x) for x in json.loads(raw)]

    def _save(self) -> None:
        data = [t.to_dict() for t in self._tasks.values()]
        self.db_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- commandes ---
    def add(self, title: str, description: str = "", due: Optional[date] = None) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Le titre ne peut pas être vide.")
        t = Task(id=self._next_id, title=title, description=description, due=due)
        self._tasks[t.id] = t
        self._next_id += 1
        self._save()
        return t

    def done(self, task_id: int) -> Task:
        t = self._tasks.get(task_id)
        if not t:
            raise KeyError(f"Tâche {task_id} introuvable.")
        t.done = True
        self._save()
        return t

    def remove(self, task_id: int) -> None:
        if task_id not in self._tasks:
            raise KeyError(f"Tâche {task_id} introuvable.")
        del self._tasks[task_id]
        self._save()

    def clear(self, done_only: bool = False) -> int:
        before = len(self._tasks)
        if done_only:
            self._tasks = {i: t for i, t in self._tasks.items() if not t.done}
        else:
            self._tasks.clear()
        self._save()
        return before - len(self._tasks)

    # --- requêtes ---
    def list(self, include_done: bool = True) -> List[Task]:
        items = list(self._tasks.values())
        if not include_done:
            items = [t for t in items if not t.done]
        items.sort(key=lambda t: (t.done, t.due or date.max))
        return items

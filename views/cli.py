from __future__ import annotations
import argparse
from datetime import date
from typing import Optional

from controllers.task_controller import TaskController

def parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        raise argparse.ArgumentTypeError("Date invalide (format attendu: YYYY-MM-DD)")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="Mini ToDo (MVC)")
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Ajouter une tâche")
    add.add_argument("title")
    add.add_argument("-d", "--description", default="")
    add.add_argument("--due", type=parse_date)

    sub.add_parser("list", help="Lister les tâches").add_argument(
        "-A", "--all", action="store_true", help="Inclure les tâches terminées"
    )

    done = sub.add_parser("done", help="Marquer comme terminée")
    done.add_argument("id", type=int)

    rm = sub.add_parser("remove", help="Supprimer une tâche")
    rm.add_argument("id", type=int)

    clr = sub.add_parser("clear", help="Effacer des tâches")
    clr.add_argument("--done", action="store_true", help="Seulement les terminées")

    return p

def render_table(tasks) -> None:
    if not tasks:
        print("(aucune tâche)")
        return
    print("ID | Titre                  | Terminé | Échéance")
    print("---+------------------------+---------+----------")
    for t in tasks:
        due = t.due.isoformat() if t.due else "-"
        print(f"{t.id:>2} | {t.title[:22]:<22} | {'oui' if t.done else 'non ':<7} | {due}")

def main(argv: list[str] | None = None) -> int:
    ctl = TaskController()
    args = build_parser().parse_args(argv)

    try:
        if args.cmd == "add":
            t = ctl.add(args.title, description=args.description, due=args.due)
            print(f"Ajoutée: #{t.id} « {t.title} »")
        elif args.cmd == "list":
            render_table(ctl.list(include_done=args.all))
        elif args.cmd == "done":
            t = ctl.done(args.id)
            print(f"Terminée: #{t.id} « {t.title} »")
        elif args.cmd == "remove":
            ctl.remove(args.id)
            print(f"Supprimée: #{args.id}")
        elif args.cmd == "clear":
            n = ctl.clear(done_only=args.done)
            print(f"Supprimées: {n}")
        return 0
    except (ValueError, KeyError) as e:
        print(f"Erreur: {e}")
        return 1

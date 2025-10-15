# main.py
from __future__ import annotations
import sys
from datetime import date
from controllers.task_controller import TaskController
from views.cli import main as cli_main, render_table

def _parse_due(s: str | None):
    if not s:
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        print("⚠️  Date invalide. Format: YYYY-MM-DD (ex: 2025-11-01).")
        return None

def run_menu():
    ctl = TaskController()
    while True:
        print("\n=== ToDoList ===")
        print("1) Ajouter une tâche")
        print("2) Lister les tâches")
        print("3) Marquer une tâche comme terminée")
        print("4) Supprimer une tâche")
        print("5) Effacer toutes les tâches terminées")
        print("0) Quitter")
        choice = input("Votre choix: ").strip()

        if choice == "1":
            title = input("Titre: ").strip()
            if not title:
                print("⚠️  Le titre ne peut pas être vide.")
                continue
            desc = input("Description (optionnel): ").strip()
            due_str = input("Échéance YYYY-MM-DD (laisser vide si aucune): ").strip()
            due = _parse_due(due_str)
            try:
                t = ctl.add(title, description=desc, due=due)
                print(f"✅ Ajoutée: #{t.id} « {t.title} »")
            except ValueError as e:
                print(f"⚠️  Erreur: {e}")

        elif choice == "2":
            incl = input("Inclure les terminées ? (o/N): ").strip().lower() == "o"
            render_table(ctl.list(include_done=incl))

        elif choice == "3":
            try:
                task_id = int(input("ID de la tâche: ").strip())
                t = ctl.done(task_id)
                print(f"✅ Terminée: #{t.id} « {t.title} »")
            except (ValueError, KeyError) as e:
                print(f"⚠️  Erreur: {e}")

        elif choice == "4":
            try:
                task_id = int(input("ID de la tâche: ").strip())
                ctl.remove(task_id)
                print(f"🗑️  Supprimée: #{task_id}")
            except (ValueError, KeyError) as e:
                print(f"⚠️  Erreur: {e}")

        elif choice == "5":
            n = ctl.clear(done_only=True)
            print(f"🧹 Supprimées (terminées): {n}")

        elif choice == "0":
            print("À bientôt 👋")
            break
        else:
            print("⚠️  Choix invalide. Tapez 0,1,2,3,4 ou 5.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Mode CLI existant si des arguments sont fournis
        raise SystemExit(cli_main(sys.argv[1:]))
    else:
        # Menu interactif sinon
        run_menu()

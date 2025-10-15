# ToDoList

## Utilisation et Commandes essentielles
```bash
# Ajouter une tâche
python main.py add "Acheter du café"

# Afficher les tâches (display)
python main.py list
python main.py list -A           # inclure les tâches terminées

# Marquer une tâche comme terminée
python main.py done 1

# Supprimer une tâche (delete)
python main.py remove 1

```
```
├─ main.py
├─ db.json
├─ controllers/
│  └─ task_controller.py
├─ model/
│  └─ task.py
└─ views/
   └─ cli.py
```


import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"
version = "1"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()
parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-v", "--version", help="Show current version", action="version", version=f"untitled todo program v{version}")
parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
parser.add_argument("-i", "--incomplete", type=int, help="Mark a task as incomplete by ID")
parser.add_argument("-p", "--priority", type=int, help="Toggle a task as priority by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
  
if args.list:
    tasks = load_tasks()
    if tasks == []:
        print("No tasks. Try adding one!")
    else:
        for task in tasks:
            status = "x" if task["done"] else " "
            priority = "!" if task["priority"] else " "
            print(f"[{status}] [{priority}] {task['id']}: {task['task']}")
    sys.exit(0)
elif args.complete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.complete:
            task["done"] = True
            save_task(tasks)
            print(f"Task {args.complete} marked as complete")
            break
elif args.incomplete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.incomplete:
            task["done"] = False
            save_task(tasks)
            print(f"Task {args.incomplete} marked as incomplete")
            break
elif args.priority:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.priority:
            if task["priority"] == False:
                task["priority"] = True
                save_task(tasks)
                print(f"Task {args.priority} marked as priority")
            else:
                task["priority"] = False
                save_task(tasks)
                print(f"Task {args.priority} unmarked as priority")
elif args.delete:
    tasks = load_tasks()
    new_tasks = []
    for task in tasks:
        if task["id"] != args.delete:
            new_tasks.append(task)
        tasks = new_tasks
        save_task(new_tasks)
    print(f"Task with ID of {args.delete} deleted.")
elif args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = tasks[-1]["id"] + 1

    tasks.append({"id": new_id, "task": args.task, "done": False, "priority": False})
    save_task(tasks)

    print(f"Task {args.task} added with ID of {new_id}")
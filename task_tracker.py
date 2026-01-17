"""
Task Tracker (Python CLI)

This program demonstrates:
- A menu-driven command-line application
- Using lists and dictionaries to store data
- File I/O (saving and loading tasks in JSON format)
- Basic input validation
- Clear code structure with helpful comments for explanation in a video
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# We store tasks in this file (created automatically).
DATA_FILE = "tasks.json"


# --------------------------- Data Helpers ---------------------------

def load_tasks() -> List[Dict]:
    """
    Load tasks from DATA_FILE.

    If the file does not exist yet, we return an empty list.
    If the file exists but is broken, we also return an empty list
    (so the program doesn't crash).
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # If something goes wrong reading/parsing JSON, start fresh.
        return []


def save_tasks(tasks: List[Dict]) -> None:
    """
    Save tasks to DATA_FILE as JSON.
    'indent=2' makes the JSON pretty and readable if you open tasks.json.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def next_task_id(tasks: List[Dict]) -> int:
    """
    Generate the next task id.
    We find the max existing id and add 1.
    If there are no tasks, start at 1.
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# --------------------------- Input Helpers ---------------------------

def read_int(prompt: str, min_value: int, max_value: int) -> int:
    """Read an integer from the user and validate it is within range."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            value = int(raw)
            if min_value <= value <= max_value:
                return value
        print(f"Please enter a number between {min_value} and {max_value}.")


def read_non_empty(prompt: str) -> str:
    """Read a non-empty string from the user."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be blank. Try again.")


def read_optional_date(prompt: str) -> Optional[str]:
    """
    Read an optional date in YYYY-MM-DD format.
    - If user presses Enter, return None
    - If user enters a valid date, return the normalized string
    """
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None

        try:
            dt = datetime.strptime(raw, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD (example: 2026-01-16) or press Enter to skip.")


def pause(message: str = "Press Enter to continue...") -> None:
    """Small helper to pause the program so the user can read messages."""
    input("\n" + message)


# --------------------------- Display Helpers ---------------------------

def print_header(title: str) -> None:
    """Clear-ish screen and print a simple header."""
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40 + "\n")


def list_tasks(tasks: List[Dict]) -> None:
    """Display all tasks with a friendly format."""
    print_header("YOUR TASKS")

    if not tasks:
        print("No tasks yet. Add one from the menu!")
        return

    for index, task in enumerate(tasks, start=1):
        status = "[X]" if task["is_complete"] else "[ ]"
        due = f" (Due: {task['due_date']})" if task.get("due_date") else ""
        print(f"{index}. {status} {task['title']}{due}")


# --------------------------- Menu Actions ---------------------------

def add_task(tasks: List[Dict]) -> None:
    """Add a new task to the list and save immediately."""
    print_header("ADD A TASK")

    title = read_non_empty("Task title: ")
    due_date = read_optional_date("Due date (YYYY-MM-DD) or press Enter to skip: ")

    task = {
        "id": next_task_id(tasks),
        "title": title,
        "due_date": due_date,     # can be None
        "is_complete": False
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Task added and saved!")


def mark_complete(tasks: List[Dict]) -> None:
    """Mark a task as complete using its displayed number."""
    print_header("MARK TASK COMPLETE")

    if not tasks:
        print("No tasks to mark complete.")
        return

    list_tasks(tasks)
    choice = read_int("\nEnter the task number to mark complete: ", 1, len(tasks))
    tasks[choice - 1]["is_complete"] = True
    save_tasks(tasks)

    print("Task marked complete and saved!")


def delete_task(tasks: List[Dict]) -> None:
    """Delete a task using its displayed number."""
    print_header("DELETE A TASK")

    if not tasks:
        print("No tasks to delete.")
        return

    list_tasks(tasks)
    choice = read_int("\nEnter the task number to delete: ", 1, len(tasks))
    deleted = tasks.pop(choice - 1)
    save_tasks(tasks)

    print(f"Deleted: {deleted['title']}")


# --------------------------- Main Program ---------------------------

def main() -> None:
    """
    Main entry point.
    - Load tasks at start
    - Show a menu in a loop
    - Save tasks after changes (and also provide a Save option)
    """
    tasks = load_tasks()

    while True:
        print_header("TASK TRACKER (PYTHON)")
        print("1) List tasks")
        print("2) Add a task")
        print("3) Mark task as complete")
        print("4) Delete a task")
        print("5) Save")
        print("6) Exit")

        choice = read_int("\nChoose an option (1-6): ", 1, 6)

        if choice == 1:
            list_tasks(tasks)
            pause()
        elif choice == 2:
            add_task(tasks)
            pause()
        elif choice == 3:
            mark_complete(tasks)
            pause()
        elif choice == 4:
            delete_task(tasks)
            pause()
        elif choice == 5:
            save_tasks(tasks)
            print("Saved!")
            pause()
        elif choice == 6:
            # Good practice: save before exit so nothing is lost.
            save_tasks(tasks)
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()

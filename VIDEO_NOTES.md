# Video Notes (4–5 minutes)

## 1) Intro (0:00–0:20) — Face on camera
- “Hi, I’m Cas Perche. This is my Task Tracker program in Python.”
- “I’ll demo the program and then walk through the code.”

## 2) Demo (0:20–1:40)
- Run: `python task_tracker.py`
- Add 2 tasks (one with a due date, one without)
- List tasks
- Mark one task complete
- Delete a task (optional)
- Exit and reopen to show tasks are saved/loaded from `tasks.json`

## 3) Code Walkthrough (1:40–4:30)
- Data structure: list of dictionaries (each task has id, title, due_date, is_complete)
- `load_tasks()` and `save_tasks()` using JSON
- Menu loop in `main()` and the `match`/`if` logic for choices
- Input validation helpers (`read_int`, `read_non_empty`, `read_optional_date`)
- Explain how comments guide the reader

## 4) Wrap-up (4:30–5:00) — Face on camera
- What you learned: lists/dicts, functions, JSON, file I/O, validation
- Future improvements: priorities, sorting, search

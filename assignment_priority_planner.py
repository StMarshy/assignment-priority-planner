import json
from datetime import datetime

FILE_NAME = "tasks.json"


def load_tasks():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def days_until_due(due_date_str):
    today = datetime.today().date()
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    return (due_date - today).days


def calculate_priority(task):
    days_left = max(days_until_due(task["due_date"]), 0)

    urgency_score = 100 / (days_left + 1)
    difficulty_score = task["difficulty"] * 1.5
    importance_score = task["importance"] * 2
    time_score = task["estimated_hours"] * 0.8

    total_score = urgency_score + difficulty_score + importance_score + time_score
    return round(total_score, 2)


def add_task():
    print("\n=== Add New Task ===")
    title = input("Task title: ").strip()
    course = input("Course name: ").strip()
    due_date = input("Due date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.\n")
        return

    try:
        difficulty = int(input("Difficulty (1-5): ").strip())
        estimated_hours = float(input("Estimated hours needed: ").strip())
        importance = int(input("Importance (1-5): ").strip())
    except ValueError:
        print("Please enter valid numbers.\n")
        return

    if not (1 <= difficulty <= 5):
        print("Difficulty must be between 1 and 5.\n")
        return

    if not (1 <= importance <= 5):
        print("Importance must be between 1 and 5.\n")
        return

    tasks = load_tasks()

    task = {
        "title": title,
        "course": course,
        "due_date": due_date,
        "difficulty": difficulty,
        "estimated_hours": estimated_hours,
        "importance": importance
    }

    task["priority_score"] = calculate_priority(task)
    tasks.append(task)
    save_tasks(tasks)

    print("Task added successfully.\n")


def view_tasks():
    print("\n=== All Tasks Sorted by Priority ===")
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.\n")
        return

    for task in tasks:
        task["priority_score"] = calculate_priority(task)

    tasks.sort(key=lambda x: x["priority_score"], reverse=True)
    save_tasks(tasks)

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']} ({task['course']})")
        print(f"   Due Date: {task['due_date']}")
        print(f"   Difficulty: {task['difficulty']}/5")
        print(f"   Importance: {task['importance']}/5")
        print(f"   Estimated Hours: {task['estimated_hours']}")
        print(f"   Days Left: {days_until_due(task['due_date'])}")
        print(f"   Priority Score: {task['priority_score']}")
        print()


def mark_task_complete():
    tasks = load_tasks()

    if not tasks:
        print("\nNo tasks to complete.\n")
        return

    for task in tasks:
        task["priority_score"] = calculate_priority(task)

    tasks.sort(key=lambda x: x["priority_score"], reverse=True)

    print("\n=== Mark Task Complete ===")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']} ({task['course']}) - Score: {task['priority_score']}")

    try:
        choice = int(input("Enter the task number to mark as complete: ").strip())
    except ValueError:
        print("Please enter a valid number.\n")
        return

    if 1 <= choice <= len(tasks):
        completed_task = tasks.pop(choice - 1)
        save_tasks(tasks)
        print(f"Completed and removed: {completed_task['title']}\n")
    else:
        print("Invalid task number.\n")


def main():
    while True:
        print("=== Assignment Priority Planner ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_task_complete()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()
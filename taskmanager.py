import json
import os
import sys

from tabulate import tabulate

# Import msvcrt for Windows systems
if os.name == "nt":
    import msvcrt

    def getch():
        return msvcrt.getch()


# Import termios and tty for POSIX systems
elif os.name == "posix":
    import termios
    import tty

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


if "tasks.json" not in os.listdir(os.getcwd()):
    with open("tasks.json", "x") as f:
        json.dump([], f, indent=4)


def frame_text(text):
    width = len(text) + 4
    frame = "+" + "-" * (width - 2) + "+"
    framed_text = frame + "\n"
    framed_text += "| " + text + " |\n"
    framed_text += frame + "\n"
    return framed_text


def load_tasks():
    clear_terminal()
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    return tasks


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)
    clear_terminal()


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def create_task():
    clear_terminal()
    task = input(frame_text("enter task name:"))
    description = input(frame_text("enter task description"))
    tasks = load_tasks()
    max_id = max(task["id"] for task in tasks) if tasks else 0
    id = max_id + 1
    tasks.append({"id": id, "task": task, "description": description})
    save_tasks(tasks)
    list_tasks()


def list_tasks():
    clear_terminal()
    data = load_tasks()
    table_data = []
    for task in data:
        table_data.append(
            [task.get("id", ""), task.get("task", ""), task.get("description", "")]
        )
    print(tabulate(table_data, headers=["id", "task", "description"]))


def list_task(id):
    clear_terminal()
    data = load_tasks()
    table_data = []
    for task in data:
        if task["id"] == id:
            table_data.append(
                [task.get("id", ""), task.get("task", ""), task.get("description", "")]
            )
    print(tabulate(table_data, headers=["id", "task", "description"]))


def get_choice(sentence: str) -> int:
    print(sentence)
    choice = getch()  # This will use the correct getch based on the OS
    return int(choice.decode("utf-8"))


def find_task(id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == id:
            return task


def confirm_update(tasks: list, task: dict, field: str, new_value: str) -> int:
    old_value = task[field]
    print(
        frame_text(
            f"old {field.lower()} : {old_value}\nnew {field.lower()} : {new_value}"
        )
    )
    for old_task in tasks:
        if old_task["id"] == task["id"]:
            old_task[field] = new_value
            save_tasks(tasks)
            return 0
    return 1


def update_task(id):
    while True:
        task = find_task(id) or {}
        if not task:
            print(
                frame_text("Error: Task not found or there is an issue with the JSON.")
            )
            break

        choice = get_choice(
            frame_text(
                "Update name(1), update description(2), update both(3), go back(0)"
            )
        )
        if choice == 0:
            break

        tasks = load_tasks()
        if choice == 1:
            new_name = input(frame_text("Enter new name"))
            if confirm_update(tasks, task, "task", new_name) == 0:
                print(frame_text("Task name updated successfully."))

        elif choice == 2:
            new_description = input(frame_text("Enter new description"))
            if confirm_update(tasks, task, "description", new_description) == 0:
                print(frame_text("Task description updated successfully."))

        elif choice == 3:
            new_name = input(frame_text("Enter new name"))
            new_description = input(frame_text("Enter new description"))
            if confirm_update(tasks, task, "task", new_name) == 0:
                print(frame_text("Task name updated successfully."))
            if confirm_update(tasks, task, "description", new_description) == 0:
                print(frame_text("Task description updated successfully."))

        else:
            print(frame_text("Incorrect choice. Please try again."))


def delete_task(id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != id]
    save_tasks(tasks)
    print(frame_text(f"Task {id} deleted successfully."))


def select_task():
    while True:
        clear_terminal()
        id = int(input("Enter task id: "))
        operation = get_choice(frame_text("Edit task(1), Delete task(2), Go back(0)"))
        if operation == 1:
            update_task(id)
        elif operation == 2:
            delete_task(id)
        elif operation == 0:
            break
        else:
            print("Invalid choice, please try again.")


def app():
    while True:
        list_tasks()
        selection = get_choice(
            frame_text(
                "Create new task (1), Refresh tasks (2), Select task (3), Exit (0)"
            )
        )
        if selection == 1:
            create_task()
        elif selection == 2:
            list_tasks()
        elif selection == 3:
            select_task()
        elif selection == 0:
            break
        else:
            print("Invalid Choice")


app()

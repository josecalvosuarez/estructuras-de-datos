# task_manager.py

def add_task(task):
    with open("tasks.txt", "a") as file:
        file.write(task + "\n")
    print(f"Task added: {task}")

def list_tasks():
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
            if not tasks:
                print("No tasks found.")
            else:
                print("Tasks:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task.strip()}")
    except FileNotFoundError:
        print("No task file found.")

def remove_task(task_number):
    try:
        with open("tasks.txt", "r") as file:
            tasks = file.readlines()
        if 0 < task_number <= len(tasks):
            removed = tasks.pop(task_number - 1)
            with open("tasks.txt", "w") as file:
                file.writelines(tasks)
            print(f"Removed: {removed.strip()}")
        else:
            print("Invalid task number.")
    except FileNotFoundError:
        print("No task file found.")

# Example usage
if __name__ == "__main__":
    add_task("Finish homework")
    add_task("Go for a walk")
    list_tasks()
    remove_task(1)
    list_tasks()

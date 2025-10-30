tasks = [
    {"id": 1, "title": "買牛奶", "completed": False},
    {"id": 2, "title": "寫程式", "completed": False},
    {"id": 3, "title": "打掃家裡", "completed": True},
]

def get_tasks():
    return tasks

def add_task(title):
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    tasks.append({"id": new_id, "title": title, "completed": False})

def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]

def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
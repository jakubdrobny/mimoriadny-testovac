import os, json

def get_task_content(task_id):
    task_id = str(task_id)
    with open(os.getcwd() + "/ulohy/" + task_id + "/content.txt", 'r') as f:
        return f.read()

def get_task_info(task_id):
    task_id = str(task_id)
    with open(os.getcwd() + "/ulohy/" + task_id + "/spec.json", 'r') as f:
        return json.load(f)

def get_tasks():
    return os.listdir(os.getcwd() + "/ulohy")

def get_task_files(task_id, io):
    task_id = str(task_id)
    tests = []
    directory = os.getcwd() + "/ulohy/" + task_id + "/" + io
    for filename in os.listdir(directory):
        if filename[-4:] == '.txt':
            with open(directory + "/" + filename, 'r') as f:
                tests.append(f.read())
    return tests
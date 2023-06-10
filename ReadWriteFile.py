import json
from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Task:
    id: int
    header: str
    body: str
    updated: str

    def __str__(self):
        date_string = self.updated
        date_format = '%Y-%m-%dT%H:%M:%S'
        date_output = datetime.strptime(date_string, date_format)
        return 'ID: {0}, \n\t' \
               '{1:<15}: {2}, \n\t' \
               '{3:<15}: {4}, \n\t' \
               '{5:<15}: {6}'.format(self.id, 'HEADER', self.header, 'TASK', self.body, 'LAST UPDATED', date_output)


def read_json() -> List[Task]:
    task_list = list()
    with open('task_list.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    for task in tasks:
        new_task = Task(task.get('id'),
                        task.get('header'),
                        task.get('body'),
                        task.get('updated'))
        task_list.append(new_task)

    return task_list


def write_jason(task_list):
    tasks = []
    for task in task_list:
        tasks.append(task.__dict__)
    with open('task_list.json', 'w') as f:
        json.dump(tasks, f, indent=4)

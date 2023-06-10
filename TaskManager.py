import sys
from typing import List

from ReadWriteFile import write_jason, Task
from _datetime import datetime


class TaskManager:

    def __init__(self, task_list):
        self.__task_list = task_list
        self.max_id: int = 0
        for task in task_list:
            if self.max_id < task.id:
                self.max_id = task.id

    @property
    def get_task_list(self):
        return self.__task_list

    @get_task_list.setter
    def get_task_list(self, new_task: Task):
        self.get_task_list.append(new_task)

    def run_manager(self):
        commands_list = [
            'add',
            'del',
            'pr all',
            'pr date',
            'edit',
            'save',
            'exit'
        ]

        cmd_line = ', '.join(commands_list)
        while True:
            cmd = input(f'Type in one of your wishes [{cmd_line}]: ')
            match cmd.strip().lower():
                case 'add':
                    self.add_task()
                case 'del':
                    self.del_task()
                case 'pr all':
                    self.print_all_tasks()
                case 'pr date':
                    self.print_tasks_by_date()
                case 'save':
                    self.save_all_tasks()
                case 'edit':
                    self.edit_task()
                case 'exit':
                    write_jason(self.get_task_list)
                    sys.exit()
                case _:
                    print('Can\'t execute such wish!')

    def add_task(self):
        """ Adding new task to a task list """
        self.max_id += 1
        new_task = Task(
            self.max_id,
            input('Type header of your new task: '),
            input('Type your task: '),
            str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        )
        self.get_task_list = new_task
        print('Task saved!')

    def print_all_tasks(self):
        """ Print all tasks """
        for task in self.get_task_list:
            print(task)

    def print_tasks_by_date(self):
        """ Print tasks filtered by date """
        user_input = input('Enter date to search tasks (use format \'YY-MM-DD\' - 23-06-09): ')
        no_such_date = True
        for task in self.get_task_list:
            if user_input in task.updated:
                no_such_date = False
                print(task)

        if no_such_date:
            print('No tasks for this date!')

    def print_filtered_tasks(self, task_search_list):
        counter = 1
        for task in task_search_list:
            print(counter, end=': ')
            date_string = task.updated
            date_format = '%Y-%m-%dT%H:%M:%S'
            date_output = datetime.strptime(date_string, date_format)
            print(f'HEADER: {task.header}, TASK: {task.body}, LAST UPDATED: {date_output}')
            counter += 1

    def del_task(self):
        """ Delete chosen task """
        user_input = input('Enter text to search from tasks, type \'all\' or type \'cancel\': ')
        if user_input.strip().lower() == 'cancel':
            return
        elif user_input.strip().lower() == 'all':
            task_search_list: List[Task] = [task for task in self.get_task_list]
        else:
            task_search_list: List[Task] = [task for task in self.get_task_list if
                                            user_input in task.body or user_input in task.header]

        self.print_filtered_tasks(task_search_list)
        user_choice = self.check_input(task_search_list, action='delete')
        task_to_delete = task_search_list[user_choice - 1]
        self.get_task_list.remove(task_to_delete)
        print('Task deleted!')

    def check_input(self, task_search_list, action):
        while True:
            try:
                user_input = input(f'Type task number to {action} task or type \'cancel\': ')
                if user_input.strip().lower() == 'cancel':
                    return
                user_choice = int(user_input)
                if not user_choice - 1 in range(len(task_search_list)):
                    raise IndexError
                break
            except ValueError:
                print('Wrong wish format!')
            except IndexError:
                print('Wrong wish number!')
        return user_choice

    def save_all_tasks(self):
        """ Save all the tasks from the list to a JSON """
        write_jason(self.get_task_list)
        print('Saved to file!')

    def edit_task(self):
        """ Editing header or body of chosen task """
        while True:
            user_input = input('Type \'H\' for header, \'T\' for text edit or \'cancel\': ')
            if user_input.strip().lower() == 'cancel':
                return
            match user_input:
                case 'H':
                    user_input = input('Type text to go through headers: ')
                    task_search_list: List[Task] = [task for task in self.get_task_list if user_input in task.header]
                    self.print_filtered_tasks(task_search_list)
                    user_choice = self.check_input(task_search_list, action='edit')
                    task_to_edit = task_search_list[user_choice - 1]
                    print(f'Editing header - \'{task_to_edit.header}\'')
                    user_input = input('Type edited header: ')
                    task_to_edit.header = user_input
                    task_to_edit.updated = str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                    break
                case 'T':
                    user_input = input('Type text to go through headers: ')
                    task_search_list: List[Task] = [task for task in self.get_task_list if user_input in task.body]
                    self.print_filtered_tasks(task_search_list)
                    user_choice = self.check_input(task_search_list, action='edit')
                    task_to_edit = task_search_list[user_choice - 1]
                    print(f'Editing header - \'{task_to_edit.body}\'')
                    user_input = input('Type edited body: ')
                    task_to_edit.body = user_input
                    task_to_edit.updated = str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
                    break
                case _:
                    print('Nice try, but you have to try again!')

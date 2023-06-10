from TaskManager import TaskManager
from ReadWriteFile import read_json


def main():
    tasks_list = read_json()
    task_manager = TaskManager(tasks_list)
    task_manager.run_manager()


if __name__ == '__main__':
    main()

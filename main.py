import os
from lib.Paths import Path
import sys
from lib.Task import Task


def main(argv: list, arg_c: int):
    if arg_c < 2:
        exit('too few arguments')
    command, task_name = argv[:2]
    if command == "new" and arg_c >= 4:
        if os.path.isdir(Path.generate_task_path(task_name)):
            exit('There\'s already a task with that name\nPlease choose a different name')
        print(command, task_name)
        task = Task(task_name, argv[2], argv[3])
    elif command == "resume":
        task = Task(task_name)

    task.generate_initial_list()
    print('start copying...')
    task.make_attempts()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args, len(args))

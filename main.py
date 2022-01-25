import sys
from lib.Task import Task


def main(argv: list, arg_c: int):
    if arg_c < 2:
        exit('too few arguments')
    command, task_name = argv[:2]
    if command == "new" and arg_c >= 4:
        print(command, task_name)
        task = Task(task_name, argv[2], argv[3])
        task.generate_initial_list()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args, len(args))

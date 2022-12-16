import sys
from lib.Task import Task


def main(argv: list, arg_c: int):
    if arg_c < 3:
        exit('too few arguments')
    task_name, old_path, new_path = argv[:3]
    task = Task(task_name)
    if not task.exists(task.full_path):
        exit("Task not found")
    Task(task_name).update_base_path(old_path, new_path)
    print("Task path updated.")


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args, len(args))

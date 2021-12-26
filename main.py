import json
import os
import sys


def task_exists(task_name: str) -> bool:
    return os.path.isdir(task_name)


def generate_task_path(task_name: str) -> str:
    task_base_path = "tasks/"
    return task_base_path + task_name


def json_file(file_name: str) -> dict or list or tuple:
    with open(file_name + ".json", "r") as outfile:
        return json.load(outfile.read(file_name))


def json_file(file_name: str, jsonable: dict, mode_append=False):
    json.dump(jsonable)
    with open(file_name + ".json", "a" if mode_append else "w") as outfile:
        return outfile.write(jsonable)


def initialize_task(task_name: str, source_path: str, destination_path: str):
    task_path = generate_task_path(task_name)
    if task_exists(task_path):
        print(json_file('config'))
        exit('there\'s already a task with that name\nPlease choose a different name')
    try:
        os.makedirs(task_path)
        os.makedirs(task_path + "initial_list.d")
    except OSError as e:
        print('m16')
        exit(e)
    json_file('config', {
        "source_path": source_path,
        "destination_path": destination_path
    })


def valid_path(abs_parent, child):
    if abs_parent[-1] not in ("\\", "/"):
        abs_parent += "/"
    return abs_parent+child


def generate_initial_list(source_path: str):
    init = {
        "current": "",
        "files": [],
        "remaining": [source_path]
    }
    while init['remaining']:
        init['current'] = init['remaining'].pop()
        for child in os.listdir(init['current']):
            path = valid_path(init['current'], child)
            if os.path.isdir(path):
                init['remaining'].append(path+"/")
            elif os.path.isfile(path):
                init['files'].append(path)


def main(argv: list, arg_c: int):
    if arg_c < 2:
        exit('too few arguments')
    command, task_name = argv[:2]
    if command == "new" and arg_c >= 4:
        print(command, task_name)
        initialize_task(task_name, argv[2], argv[3])
        generate_initial_list(argv[2])


if __name__ == '__main__':
    args = sys.argv[1:]
    argc = len(args)
    main(args, argc)

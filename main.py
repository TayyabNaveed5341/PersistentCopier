import os
import sys


def main(argv):
    if len(argv) < 2:
        exit('too few arguments')
    command, task_name = argv[:2]
    if command == "new":
        print(command, task_name)


if __name__ == '__main__':
    main(sys.argv[1:])

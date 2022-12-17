##
#   Original Author: Tayyab Naveed
# Description:
# selects file paths by the provided keyword
# based on choice selected paths are either:
#   skipped in the current attempt (to be tried again in the next attempt)
#   or removed and completely forgotten
##
import sys
from lib.Task import Task


def main(argv: list, arg_c: int):
    if arg_c < 3:
        exit('too few arguments')
    task_name, path_keyword, action = argv[:3]
    if action not in ("forget", "postpone"):
        exit('invalid action')
    task = Task(task_name)
    if not task.exists(task.full_path):
        exit("Task not found")
    if action == "forget":
        exit("not implemented")
    elif action == "postpone":
        postponed_file_count = task.postpone_from_current_attempt(path_keyword)
        print(str(postponed_file_count)+" files skipped.")
    print("End of program.")


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args, len(args))

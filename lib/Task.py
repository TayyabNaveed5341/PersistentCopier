import json

from lib.SavePointService import SavePointService
import time
from lib.common import Common
from lib.Paths import Path
import os
import shutil
from lib.VersionedFileDirectory import VersionedFileDirectory


class Task:
    DESTINATION_PATH: str
    INITIAL_DIRECTORY_NAME = "initial_list.d"
    ATTEMPTS_DIRECTORY_NAME = "attempts.d"
    config_file_path: str

    def __init__(self, name, source="", destination=""):
        self.DESTINATION_PATH = destination
        self.name = name
        self.full_path = Path.generate_task_path(self.name)
        self.source_path = source

        # task directory structure paths
        self.config_file_path: str = self.full_path + '/config'
        self.attempts_path: str = Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME)

        # check of the task already exists
        if self.exists(self.full_path) and (source == "" or destination == ""):
            config = Common.json_file(self.config_file_path)
            self.source_path = config["source_path"]
            self.DESTINATION_PATH = config["destination_path"]
        else:
            self.create_new()

    def abort_creation(self, message: str):
        print(message, '\nrolling back')
        shutil.rmtree(self.full_path)
        exit()

    def create_new(self):
        print('checking if the task already exists')
        if Task.exists(self.full_path):
            print('there\'s already a task with that name\nPlease choose a different name')
            exit(Common.json_file(self.config_file_path))
        try:
            os.makedirs(self.full_path)
            os.makedirs(Path.valid_path(self.full_path, self.INITIAL_DIRECTORY_NAME))
        except OSError as e:
            print('m16')
            exit(e)
        try:
            Common.json_file(self.config_file_path, {
                "source_path": self.source_path,
                "destination_path": self.DESTINATION_PATH
            })
        except BaseException as ex:
            print(ex)
            print(ex.__class__)
            self.abort_creation('XT~39 unhandled exception')

    def get_versioned_initial_list(self, age: int = 0):
        initial_list_path: str = Path.valid_path(self.full_path, self.INITIAL_DIRECTORY_NAME)
        initial_list = VersionedFileDirectory(initial_list_path).get(age)
        return json.loads(initial_list)

    def get_versioned_attempts_list(self, age: int = 0):
        attempts_list = VersionedFileDirectory(self.attempts_path)
        return json.loads(attempts_list.get(age))

    def write_versioned_attempts_list(self, data):
        Common.json_file(
            Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME + "/" + str(time.time_ns())), data
        )

    def postpone_from_current_attempt(self, path_keyword: str):
        attempt = self.get_versioned_attempts_list()
        kept = []
        postponed_file_count: int = 0
        for path in attempt["queue"]:
            if path_keyword in path:
                attempt["failed"].append(path)
                postponed_file_count += 1
            else:
                kept.append(path)
        attempt["queue"] = kept
        self.write_versioned_attempts_list(attempt)
        return postponed_file_count

    def update_base_path(self, old_path, new_path):
        print("Reading initial list")
        initial_list: dict = self.get_versioned_initial_list()
        print("updating paths")
        initial_list["files"] = [path.replace(old_path, new_path) for path in initial_list["files"]]
        initial_list["remaining"] = [path.replace(old_path, new_path) for path in initial_list["remaining"]]
        initial_list["failed"] = [path.replace(old_path, new_path) for path in initial_list["failed"]]
        print("Writing updated paths")
        Common.json_file(
            Path.valid_path(self.full_path, self.INITIAL_DIRECTORY_NAME+"/"+str(time.time_ns())), initial_list
        )

        print("Reading attempts")
        if self.exists(self.attempts_path):
            attempts_list = self.get_versioned_attempts_list()
            print("updating paths")
            attempts_list["queue"] = [path.replace(old_path, new_path) for path in attempts_list["queue"]]
            attempts_list["failed"] = [path.replace(old_path, new_path) for path in attempts_list["failed"]]
            print("Writing updated paths")
            Common.json_file(
                Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME + "/" + str(time.time_ns())),
                attempts_list
            )

    def generate_initial_list(self):
        if self.exists(Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME)):
            return True
        initial_path: str = Path.valid_path(self.full_path, self.INITIAL_DIRECTORY_NAME)

        if self.exists(initial_path) and len(os.listdir(initial_path)) > 0:
            print("Found previous progress")
            init = self.get_versioned_initial_list()
        else:
            init = {
                "current": "",
                "files": [],
                "remaining": [self.source_path],
                "failed": []
            }
        save_point_service = SavePointService(init, Path.valid_path(self.full_path, self.INITIAL_DIRECTORY_NAME))
        while init['remaining']:
            init['current'] = init['remaining'].pop()
            print(init['current'])
            time.sleep(0.0625)
            try:
                for child in os.listdir(init['current']):
                    save_point_service.run_pending()
                    path = Path.valid_path(init['current'], child)
                    if os.path.isdir(path):
                        init['remaining'].append(path + "/")
                    elif os.path.isfile(path):
                        init['files'].append(path)
            except OSError as osError:
                print("unable to read directory contents")
                init["failed"].append(init["current"])
        init['current'] = ""
        save_point_service.backup()
        del save_point_service

    def make_attempts(self):
        print('t~90')
        initial = self.get_versioned_initial_list()
        attempts_path: str = Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME)
        if self.exists(attempts_path):
            attempt = self.get_versioned_attempts_list()
        else:
            try:
                os.makedirs(Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME))
            except OSError as e:
                print("XT~102")
                exit(e)
            attempt = {
                "counter": 0,
                "current": "",
                "queue": initial["files"],
                "failed": []
            }
        save_point_service = SavePointService(attempt, attempts_path)
        while attempt["queue"] or attempt["failed"]:
            while attempt["queue"]:
                attempt["current"] = attempt["queue"].pop()
                try:
                    dst = attempt["current"].replace(self.source_path, self.DESTINATION_PATH).rsplit("/", 1)[0]
                    print("Copying... " + attempt["current"])
                    print("To " + dst)
                    os.makedirs(dst, exist_ok=True)
                    shutil.copy(attempt["current"], dst)
                except FileNotFoundError as fileNotFoundError:
                    print("NOT FOUND")
                    choice = input("What would you like to do:\n(1) Skip forever\n(2) Try later\n(3)Terminate program\nEnter choice:")
                    if choice == "1":
                        print("File skipped and forgotten")
                    elif choice == "2":
                        attempt["failed"].append(attempt["current"])
                        print("Will try again in next iteration")
                    else:
                        del save_point_service
                        exit("program terminated")

                except BaseException as be:
                    print(be.__class__)
                    attempt["failed"].append(attempt["current"])

                finally:
                    save_point_service.run_pending()
            if attempt["failed"]:
                attempt["queue"] = attempt["failed"]
                attempt["failed"] = []
                attempt["counter"] += 1
                save_point_service.backup()
                print("Failed to copy " + len(attempt["queue"]).__str__() + " files")
                print("retrying...")
        del save_point_service

    @staticmethod
    def exists(task_name: str) -> bool:
        return os.path.isdir(task_name)

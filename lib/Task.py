import json

from lib.SavePointService import SavePointService
from lib.common import Common
from lib.Paths import Path
import os
from time import sleep
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
        self.config_file_path: str = self.full_path + '/config'
        if self.exists(self.full_path) and (source == "" or destination == ""):  # check of the task already exists
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
                "remaining": [self.source_path]
            }
        save_point_service = SavePointService(init, Path.valid_path(self.full_path, self.INITIAL_DIRECTORY_NAME))
        while init['remaining']:
            init['current'] = init['remaining'].pop()
            print(init['current'])
            sleep(0.0625)
            for child in os.listdir(init['current']):
                save_point_service.run_pending()
                path = Path.valid_path(init['current'], child)
                if os.path.isdir(path):
                    init['remaining'].append(path + "/")
                elif os.path.isfile(path):
                    init['files'].append(path)
        init['current'] = ""
        save_point_service.backup()
        del save_point_service

    def make_attempts(self):
        print('t~90')
        initial = self.get_versioned_initial_list()
        attempts_path: str = Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME)
        if self.exists(attempts_path):
            attempts_list = VersionedFileDirectory(attempts_path)
            attempt = json.loads(attempts_list.get())
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
                    exit('NOT FOUND')
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

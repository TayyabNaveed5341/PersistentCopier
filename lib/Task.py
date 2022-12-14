from lib.SavePointService import SavePointService
from lib.common import Common
from lib.Paths import Path
import os
from time import sleep
import shutil

class Task:
    DESTINATION_PATH: object
    INITIAL_DIRECTORY_NAME = "initial_list.d"
    ATTEMPTS_DIRECTORY_NAME = "attempts.d"

    def __init__(self, name, source="", destination=""):
        self.DESTINATION_PATH = destination
        self.name = name
        self.full_path = Path.generate_task_path(self.name)
        self.source_path = source

        #if(False):  # check of the task already exists
            #   TODO: resume
        #else:
        self.create_new()

    def abort_creation(self, message: str):
        print(message, '\nrolling back')
        shutil.rmtree(self.full_path)
        exit()

    def create_new(self):
        config_file_path: str = self.full_path + '/config'
        print('checking if the task already exists')
        if Task.exists(self.full_path):
            print('there\'s already a task with that name\nPlease choose a different name')
            exit(Common.json_file(config_file_path))
        try:
            os.makedirs(self.full_path)
            os.makedirs(Path.valid_path(self.full_path, self.INITIAL_DIRECTORY_NAME))
        except OSError as e:
            print('m16')
            exit(e)
        try:
            Common.json_file(config_file_path, {
                "source_path": self.source_path,
                "destination_path": self.DESTINATION_PATH
            })
        except BaseException as ex:
            print(ex)
            print(ex.__class__)
            self.abort_creation('XT~39 unhandled exception')

    def generate_initial_list(self):
        if os.path.isdir(Path.valid_path(self.full_path, self.ATTEMPTS_DIRECTORY_NAME)):
            return True
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
        save_point_service.backup()
        del save_point_service

    @staticmethod
    def exists(task_name: str) -> bool:
        return os.path.isdir(task_name)

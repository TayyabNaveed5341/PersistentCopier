import json
import os
import traceback
from multipledispatch import dispatch


class Common:
    @staticmethod
    @dispatch(str)
    def json_file(file_name: str) -> dict or list or tuple:
        complete_file_name = file_name + ".json"
        print('c~12 reading JSON file ' + complete_file_name)
        data: dict or list or tuple
        try:
            text_file = open(complete_file_name, "r")
            # read whole file to a string
            data = json.load(text_file)
            # close file
            text_file.close()
        except BaseException as be:
            print(be.__class__)
            traceback.print_exc()
            exit('Xc~21 File not found')
        return data

    @staticmethod
    @dispatch(str, dict, mode_append=bool)
    def json_file(file_name: str, jsonable: dict, mode_append: bool = False):
        with open(file_name + ".json", "a" if mode_append else "w") as outfile:
            json.dump(jsonable, outfile)
            # return outfile.write(jsonable)

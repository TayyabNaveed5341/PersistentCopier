import json


class Common:
    @staticmethod
    def json_file(file_name: str) -> dict or list or tuple:
        with open(file_name + ".json", "r") as outfile:
            return json.load(outfile.read(file_name))

    @staticmethod
    def json_file(file_name: str, jsonable: dict, mode_append=False):
        with open(file_name + ".json", "a" if mode_append else "w") as outfile:
            json.dump(jsonable, outfile)
            # return outfile.write(jsonable)

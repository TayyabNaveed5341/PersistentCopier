import json
from multipledispatch import dispatch


class Common:
    @staticmethod
    @dispatch(str)
    def json_file(file_name: str) -> dict or list or tuple:
        try:
            with open(file_name + ".json", "r") as outfile:
                print(outfile.__class__)
                print(outfile.read())
                return json.load(outfile.read())
        except FileNotFoundError:
            exit('Xc~13 task config not found')
        except Exception as bx:
            print(bx)
            #print(bx.with_traceback(bx))
            exit('Xc~15 unhandled exception')

    @staticmethod
    @dispatch(str, dict, mode_append=bool)
    def json_file(file_name: str, jsonable: dict, mode_append: bool = False):
        with open(file_name + ".json", "a" if mode_append else "w") as outfile:
            json.dump(jsonable, outfile)
            # return outfile.write(jsonable)

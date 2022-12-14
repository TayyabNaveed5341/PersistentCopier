import os


class VersionedFileDirectory:
    DIRECTORY_PATH: str = ""
    FILE_EXTENSION: str

    def __init__(self, full_path):
        self.DIRECTORY_PATH = full_path

    # returns the nth most recent version of the file with 0 being the most recent
    def get(self, last=0):
        content_list = os.listdir(self.DIRECTORY_PATH)
        content_list.sort(reverse=True)
        file_contents = ""
        with open(self.DIRECTORY_PATH+"/"+content_list[last], "r") as outfile:
            print("Reading "+last.__str__()+"th versioned file")
            file_contents = outfile.read()
        return file_contents

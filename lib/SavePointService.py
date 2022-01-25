import time

import schedule

from lib.common import Common


class SavePointService:
    def __init__(self, source, target_location: str, minutes: int = 1):
        self.minutes = minutes
        self.source_var = source
        self.target_location = target_location
        print('sp dir to ', self.target_location)

        # self.service = schedule.every(minutes).minutes.do(self.backup)
        self.service = schedule.every(minutes).seconds.do(self.backup)

        print('performing test write')
        self.backup()

    def run_pending(self):
        schedule.run_pending()

    def target(self, stamp):
        return self.target_location+'/'+str(stamp)

    def backup(self):
        print('saved')
        Common.json_file(self.target(time.time_ns()), self.source_var)

    def __del__(self):
        schedule.cancel_job(self.service)

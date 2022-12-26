import datetime

class WeekSeeker:
    def __init__(self):
        self.cur_date = datetime.datetime.now()
    def get_week(self):
        w = "W: {0}"
        return  w.format(self.cur_date.strftime('%V'))
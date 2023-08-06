# credits https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python

import time
from datetime import datetime, timedelta


class AllMatch(set):
    def __contains__(self, item): return True  # match everything


_allMatch = AllMatch()


def _to_set(obj):
    if obj is None:
        return _allMatch
    if isinstance(obj, int):
        return {obj}  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj


class Event(object):
    def __init__(self, action, sec=None, min=None, hour=None,
                 day=None, month=None, dow=None,
                 args=(), kwargs={}):
        self.secs = _to_set(sec)
        self.mins = _to_set(min)
        self.hours = _to_set(hour)
        self.days = _to_set(day)
        self.months = _to_set(month)
        self.dow = _to_set(dow)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t: datetime):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.second in self.secs) and
                (t.minute in self.mins) and
                (t.hour in self.hours) and
                (t.day in self.days) and
                (t.month in self.months) and
                (t.weekday() in self.dow))

    def check(self, t: datetime):
        if self.matchtime(t):
            self.action(*self.args, **self.kwargs)


class CronTab(object):
    def __init__(self, *events):
        self.events = events

    def run_thread(self):
        import threading
        th = threading.Thread(target=self.run, daemon=True)
        th.start()

    def run(self):
        t = datetime(*datetime.now().timetuple()[:6])
        while True:

            t += timedelta(seconds=1)
            while datetime.now() < t:
                time.sleep((t - datetime.now()).seconds)

            for e in self.events:
                e.check(t)


def main():
    action = lambda arg: print(f' {datetime.now()} happened {arg}')
    event1 = Event(action, args=(1,))
    event2 = Event(action, sec={5, 10, 30, 45, 50}, args=(2,))
    CronTab(event1, event2).run()


if __name__ == '__main__':
    main()

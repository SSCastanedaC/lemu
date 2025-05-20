"""
Using Chain of Responsibility design pattern,
"""

from datetime import datetime, timezone

class TimeFormatterHandler():
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return None

    def to_str(self, datetime_dt):
        return datetime_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

class SecondsFormatter(TimeFormatterHandler):
    def handle(self, request) -> str | None:
        if 9 <= len(str(request)) <= 11:
            request = int(request)
            datetime_dt = datetime.fromtimestamp(request, tz=timezone.utc)
            datetime_str = super().to_str(datetime_dt)
            return datetime_str
        else:
            return super().handle(request)

class MilisecondsFormatter(TimeFormatterHandler):
    def handle(self, request) -> str | None:
        if 12 <= len(str(request)) <= 14:
            request = int(request)/1000
            datetime_dt = datetime.fromtimestamp(request, tz=timezone.utc)
            datetime_str = super().to_str(datetime_dt)
            return datetime_str
        else:
            return super().handle(request)

class StringFormatter(TimeFormatterHandler):
    def handle(self, request) -> str | None:
        if "T" or " " in request:
            if "T" in request:
                sep = "T"
            if " " in request:
                sep = " "
            if "." not in request:
                request = request + ".000"
            if "Z" in request:
                request = request[:-1]
            date_format = '%Y-%m-%d' + sep + '%H:%M:%S.%f'
            datetime_dt = datetime.strptime(request, date_format)
            datetime_str = super().to_str(datetime_dt)
            return datetime_str
        else:
            return super().handle(request)


def format_datetime(datetime_str) -> str:
    msf = MilisecondsFormatter()
    scf = SecondsFormatter()
    strf = StringFormatter()
    msf.set_next(scf).set_next(strf).set_next(None)
    return msf.handle(datetime_str)

"""
assert time_handler.handle(1726668850124) == "2024-09-18T14:14:10.124Z"
assert time_handler.handle('1726668850124') == "2024-09-18T14:14:10.124Z"
assert time_handler.handle(1726667942) == "2024-09-18T13:59:02.000Z"
assert time_handler.handle('1726667942') == "2024-09-18T13:59:02.000Z"
assert time_handler.handle(969286895000) == "2000-09-18T14:21:35.000Z"
assert time_handler.handle('969286895000') == "2000-09-18T14:21:35.000Z"
assert time_handler.handle(3336042095) == "2075-09-18T14:21:35.000Z"
assert time_handler.handle('3336042095') == "2075-09-18T14:21:35.000Z"
assert time_handler.handle(3336042095000) == "2075-09-18T14:21:35.000Z"
assert time_handler.handle('3336042095000') == "2075-09-18T14:21:35.000Z"
assert time_handler.handle('2021-12-03T16:15:30.235Z') == "2021-12-03T16:15:30.235Z"
assert time_handler.handle('2021-12-03 16:15:30.235Z') == "2021-12-03T16:15:30.235Z"
assert time_handler.handle('2021-12-03T16:15:30.235') == "2021-12-03T16:15:30.235Z"
assert time_handler.handle('2021-12-03 16:15:30.235') == "2021-12-03T16:15:30.235Z"
assert time_handler.handle('2021-10-28T00:00:00.000') == "2021-10-28T00:00:00.000Z"
assert time_handler.handle('2021-10-28 00:00:00.000') == "2021-10-28T00:00:00.000Z"
assert time_handler.handle('2011-12-03T10:15:30') == "2011-12-03T10:15:30.000Z"
assert time_handler.handle('2011-12-03 10:15:30') == "2011-12-03T10:15:30.000Z"
"""

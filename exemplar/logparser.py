"""
Log parser
"""
from datetime import datetime, tzinfo, timedelta

from dateutil import parser


class UTC(tzinfo):
    ZERO = timedelta(0)

    def utcoffset(self, dt):
        return UTC.ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return UTC.ZERO

    def __repr__(self):
        return "UTC"


class LogEntry(object):
    """
    Create an object of the event logs
    """
    EPOCH = parser.parse("1970-01-01T00:00:00 UTC")

    def __init__(self, hostname, timestamp, filename, data):
        self.hostname = hostname
        # Thu Feb 20 10:22:04.252 PST 2014
        self.timestamp = parser.parse(timestamp)
        self.filename = filename
        self._data = data

    def __repr__(self):
        return "LogEntry({}, {}, {})".format(self.hostname,
                                             self.timestamp,
                                             self.filename,
                                             self._data,)

    def __eq__(self, other):
        return (self.auth == other.auth
                and self.timestamp == other.timestamp
                and self.filename == other.filename
                and self._data == other._data)

    @property
    def time_invoked(self):
        """
        Convert event data timestamp to a datetime (in UTC).

        Example:

            2014-02-20T18:22:03
        """
        parsed = parser.parse(self._data["timeInvoked"])
        utc_parsed = parsed.replace(tzinfo=UTC())
        tz_parsed = utc_parsed.astimezone(self.timestamp.tzinfo)
        return tz_parsed

    @property
    def since_epoch(self):
        return (self.time_invoked - LogEntry.EPOCH).total_seconds()

    @property
    def event(self):
        return self._data["event"]

    @property
    def auth(self):
        return self._data["auth"]

    @property
    def duration(self):
        return float(self._data["durationMs"]) / 1000.0

    @property
    def lag(self):
        return (self.timestamp - self.time_invoked).total_seconds()

    @classmethod
    def parse(cls, line):
        """
        Construct a LogEntry from a log line.
        """
        parts = line.split("|")
        if len(parts) != 4:
            raise Exception("Malformed log line: {}".format(line))
        hostname, timestamp, filename = parts[0:3]
        data = dict([entry.split("=", 1) for entry in parts[3].strip().split(",")])
        return cls(hostname=hostname.strip(),
                   timestamp=timestamp.strip(),
                   filename=filename.strip(),
                   data=data)

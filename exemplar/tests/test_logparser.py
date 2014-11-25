"""
Tests for log parsing.
"""
from datetime import datetime
from textwrap import dedent

from dateutil.tz import tzlocal
from nose.tools import eq_

from exemplar.logparser import LogEntry


def test_parser():
    """
    Verify that log parsing returns an object with correct fields.
    """
    line = dedent("""\
       server-api1 | Thu Feb 20 10:22:04.252 PST 2014 | finderapi.log | event=AccountService.getAssetsForFeatureAndStatus,timeInvoked=2014-02-20T18:22:03,durationMs=415,auth=IQ4eIBrEaZkuAWST,success=true,clientIdentifier=myVerizon-web""")  # noqa
    log_entry = LogEntry.parse(line)

    expected_timestamp = datetime(2014, 2, 20, 10, 22, 4, 252000, tzinfo=tzlocal())
    expected_time_invoked = datetime(2014, 2, 20, 10, 22, 3, 0, tzinfo=tzlocal())

    eq_(log_entry.hostname, "server-api1")
    eq_(log_entry.timestamp, expected_timestamp)
    eq_(log_entry.time_invoked, expected_time_invoked)
    eq_(log_entry.event, "AccountService.getAssetsForFeatureAndStatus")
    eq_(log_entry.auth, "IQ4eIBrEaZkuAWST")
    eq_(log_entry.duration, 0.415)
    eq_(log_entry.lag, 1.252)

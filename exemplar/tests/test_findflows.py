"""
test for findflows.py
"""
from os.path import dirname, join

from nose.tools import eq_

from exemplar.logparser import LogEntry
from exemplar.findflows import find_flows


def test_findflows():
    """
    Verify the flows in the flows.txt exist
    """
    with open(join(dirname(__file__), "data/flows.txt")) as file_expected:
        flows_lines = file_expected.readlines()

    with open(join(dirname(__file__), "data/testdata.log")) as file_:
        lines = file_.readlines()

    log_entries = [LogEntry.parse(line) for line in lines]

    found_flows = find_flows(flows_lines, log_entries)

    expected = {'m_lock_settings.py': 100.0}

    eq_(found_flows, expected)
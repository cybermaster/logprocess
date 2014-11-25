"""
Command line entry point.
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime
from fnmatch import filter
from gzip import GzipFile
from os import walk
from os.path import dirname, join

from exemplar.logparser import LogEntry
from exemplar.findflows import find_flows
from exemplar.report import print_report


def iter_paths(directory):
    for dirpath, dirnames, filenames in walk(directory):
        for filename in filter(filenames, '*.gz'):
            yield join(dirpath, filename)


def iter_logfiles(directory):
    for path in iter_paths(directory):
        with GzipFile(path) as logfile:
            yield logfile


def iter_lines(logfile):
    for line in logfile:
        yield line.strip()


def iter_entries(logfile):
    for line in iter_lines(logfile):
        yield LogEntry.parse(line)


def print_entries(entries):
    for entry in entries:
        print entry.auth, entry.event


def main():
    start = datetime.now()
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--directory',
                        '-d',
                        required=True,
                        help="Directory from which to load log files")
    parser.add_argument('--classify',
                        '-c',
                        action='store_true')
    args = parser.parse_args()
    argsdict = vars(args)

    for logfile in iter_logfiles(args.directory):
        entries = iter_entries(logfile)

        with open(join(dirname(__file__), "tests/data/flows.txt")) as file_expected:
            expected_flows = file_expected.readlines()

        if args.classify:
            find_flows(expected_flows, entries)
        else:
            print_report(entries)

    delta = (datetime.now() - start)
    print "The report ran for {}".format(str(delta))
"""
Classifier.py
"""
from collections import defaultdict

from exemplar.page import Page


def classify(entries):
    """
    Classify log entries into pages.

    :param entries: an iterable of LogEntry
    :return: a dictionary mapping LogEntry auth keys to list of Page objects {'authid': [page1, page2]}
    """
    by_auth = defaultdict(list)

    for entry in entries:
        by_auth[entry.auth].append(entry)

    return {key: group_by_time(value)
            for key, value in by_auth.items()}


def group_by_time(entries, time_delta=3.0):
    """
    Partition list of entries for a single auth key into multiple lists,
    based on a maximum time delta (in seconds).  The min and the max in
    each of the Page obj event list will not succeed the time_delta.

    :param entries: an iterable of LogEntry
    :param time_delta: time in seconds
    :return: a list of Pages [Page('authid', ['event1', 'event2']), Page('authid', ['e5', 'e6'])]
    """
    # anonymous function: by_time
    by_time = lambda item: item.since_epoch
    sorted_entries = sorted(entries, key=by_time)

    # start_time of the log entry
    start_time = entries[0].since_epoch
    # final_lists is list of pages
    final_lists = []
    # current_pages is list of events
    current_page = Page()

    for entry in sorted_entries:
        if (entry.since_epoch - start_time) <= time_delta:
            current_page.name = entry.auth
            current_page.add(entry.event)
        else:
            final_lists.append(current_page)
            start_time = entry.since_epoch
            current_page = Page(entry.auth, [entry.event])
    # added the last list to final_list
    final_lists.append(current_page)

    return final_lists

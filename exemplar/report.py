"""
report.py
"""
from __future__ import division
from collections import defaultdict, Counter
from operator import itemgetter

from classifier import classify


def calculate_page_percentages(entries):
    """
    create report by events per page

    :param entries: an iterable of LogEntry
    """
    classified_log = classify(entries)

    page_occurrence_result = page_occurrence(classified_log)

    result = calculate_percentage(classified_log, page_occurrence_result)

    return result


def page_occurrence(classified_log):
    """
    calculate page occurrence in all the logs

    :param classified_log: a dictionary of classified log
    :return: page_occurrence_dict: occurrence of a page
    :return: total_pgs
    """

    # {key : value};  key = hash(frozenset['e1', 'e2']);  value = number of occurrence
    page_occurrence_dict = defaultdict(int)

    for pages in classified_log.values():
        for page in pages:
            # store the list of events as a hash number and using it as a key
            pg_key = hash(frozenset(page.events))

            if page_occurrence_dict[pg_key]:
                page_occurrence_dict[pg_key] += 1
            else:
                page_occurrence_dict[pg_key] = 1

    return page_occurrence_dict


def calculate_percentage(classified_log, page_occurrence_dict):
    """
    calculate the percentage of a page

    :param classified_log: a dictionary of classified log
    :param page_occurrence_dict: occurrence of a page
    :return: result
    """
    # {[page.events]: percentage of page}
    result = defaultdict(float)

    # total number of pages
    total_pgs = sum(Counter(page_occurrence_dict).values())

    for pages in classified_log.values():
        for page in pages:
            pg_key = hash(frozenset(page.events))
            result[frozenset(page.events)] = page_occurrence_dict[pg_key] / total_pgs * 100

    return result


def print_report(entries):
    """
    Print the report to standard output

    :param entries: an iterable of LogEntry
    """
    result = calculate_page_percentages(entries)

    sorted_result = sorted(result.items(), key=itemgetter(1))

    # print the output
    # for key, value in result.items():
    #     print "{0}, {1:0.4f}%".format(key, value)

    with open('/Users/bill.zhao/sorted_output.txt', 'w') as file_to_write:
        for element in sorted_result:
            file_to_write.write(str(element) + '\n')

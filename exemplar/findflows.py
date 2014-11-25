"""
findflows.py
"""
from collections import defaultdict, Counter

from exemplar.classifier import classify
from exemplar.report import page_occurrence


def find_flows(lines, entries):
    """
    find the flows from the api_test

    :param lines: the file that has the expected flows
    :param entries: an iterable of LogEntry
    :return: found flows and percentage {'flow name': percentage}
    """
    expected_flows = get_expected_flows(lines)
    actual_flows = generate_actual_page(entries)
    intersection_flows = defaultdict(float)

    for key in expected_flows:
        if key in actual_flows:
            intersection_flows[expected_flows[key]] = actual_flows[key]

    result = get_percentage(intersection_flows)

    with open('/Users/bill.zhao/found_flows.txt', 'w') as f:
        f.write(str(result))

    return result


def get_percentage(found_flows):
    """
    get the percentage for the found_flows

    :param found_flows: the flows in common with both actual and expected flows
    :return: result: calculated the percentage each flows {'flow name': percentage}
    """

    total_pages = sum(Counter(found_flows).values())
    result = defaultdict(float)

    # calcuate the percentage
    for key, value in found_flows.items():
        result[key] = round(value / float(total_pages) * 100.0, 5)

    return result


def get_expected_flows(lines):
    """
    get the expected flows from the api_test (store as text file; it has list of the flows)

    :param lines: lines in the file
    :return: flows_dict: dict store the expected pages {hash({e1, e2, e3}: 'summary_calls.py'}
    key = hashcode of a set of api calls, value = name of flows
    """
    flows_dict = defaultdict()

    for line in lines:
        key = hash(frozenset([word.strip() for word in line.split(':')[1].split(',')]))
        value = line.split(':')[0]
        flows_dict[key] = value

    return flows_dict


def generate_actual_page(entries):
    """
    create report by events per page

    :param entries: an iterable of LogEntry
    :return: page_occurrence_result: occurrence of a page
    """
    classified_log = classify(entries)

    page_occurrence_result = page_occurrence(classified_log)

    # with open('/Users/bill.zhao/pg_occ2.txt', 'w') as f:
    #     f.write(str(page_occurrence_result))

    return page_occurrence_result
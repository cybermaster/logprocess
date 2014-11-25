"""
comparisonFunction.py
"""
from collections import defaultdict

from exemplar.report import calculate_page_percentages


def comparefunction(entries, expected):
    """
    compare the result from the classifier to the expected result
    """

    result = calculate_page_percentages(entries)

    comparison_delta = defaultdict()

    for key, value in result.items():
        comparison_delta[key] = abs(expected[key] - value)

    return comparison_delta
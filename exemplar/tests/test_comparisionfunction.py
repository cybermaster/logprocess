"""
test comparison function
"""
from os.path import dirname, join

from nose.tools import eq_

from exemplar.comparisonfunction import comparefunction
from exemplar.logparser import LogEntry
from exemplar.report import calculate_page_percentages


def test_comparisonfunction():
    """
    Verify the comparison function
    """

    with open(join(dirname(__file__), "data/testdata.log")) as file_:
        lines = file_.readlines()

    log_entries = [LogEntry.parse(line) for line in lines]

    expected_percentage = calculate_page_percentages(log_entries)

    inputs = comparefunction(log_entries, expected_percentage)

    expected = {frozenset(['AuthService.auth',
                           'ActivityWindowService.getActivityWindowsForAsset',
                           'AccountService.getAssetsForFeatureAndStatus',
                           'ImageService.getAssetImageData']): 0,
                frozenset(['AccountService.getAssetsForFeatureAndStatus']): 0,
                frozenset(['AccountService.getAccountData']): 0}

    eq_(inputs, expected)

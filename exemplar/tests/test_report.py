"""
test for report
"""
from os.path import dirname, join

from nose.tools import eq_

from exemplar.logparser import LogEntry
from exemplar.page import Page
from exemplar.report import calculate_page_percentages


def test_report():
    """
    Verify the by_page report create the page (authID), events (API calls), %
    """
    with open(join(dirname(__file__), "data/testdata.log")) as file_:
        lines = file_.readlines()

    log_entries = [LogEntry.parse(line) for line in lines]

    expected = {frozenset(['AuthService.auth',
                           'ActivityWindowService.getActivityWindowsForAsset',
                           'AccountService.getAssetsForFeatureAndStatus',
                           'ImageService.getAssetImageData']): 25.0,
                frozenset(['AccountService.getAssetsForFeatureAndStatus']): 50.0,
                frozenset(['AccountService.getAccountData']): 25.0}

    eq_(calculate_page_percentages(log_entries), expected)
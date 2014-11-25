"""
test for classifier
"""
from os.path import dirname, join

from nose.tools import eq_

from exemplar.classifier import classify
from exemplar.logparser import LogEntry
from exemplar.page import Page


class TestObject(object):
    """
    Replacement object for classification.

    Emulates LogEntry but provides a simpler model.
    """

    def __init__(self, since_epoch, auth, event):
        self.since_epoch = since_epoch
        self.auth = auth
        self.event = event

    def __eq__(self, other):
        return self.since_epoch == other.since_epoch and self.auth == other.auth

    def __repr__(self):
        return "TestObject({}, {})".format(self.since_epoch,
                                           self.auth)


def test_classify_log_entry():
    """
    Verify that classify processes an object with correct fields.
    The test base on the LogEntry object
    """

    with open(join(dirname(__file__), "data/testdata.log")) as file_:
        lines = file_.readlines()

    log_entries = [LogEntry.parse(line) for line in lines]

    expected = {
        "hGIfhCzvUi77vt9": [Page("hGIfhCzvUi77vt9", ["AuthService.auth",
                                                       "AccountService.getAssetsForFeatureAndStatus",
                                                       "ImageService.getAssetImageData",
                                                       "ActivityWindowService.getActivityWindowsForAsset"])],
        "CDKGLBCziaGTDX": [Page("CDKGLBCziaGTDX", ["AccountService.getAccountData"])],
        "fhKhSeq4Ba0tQ9": [Page("fhKhSeq4Ba0tQ9", ["AccountService.getAssetsForFeatureAndStatus"])],
        "9OroBz49b9ycXw": [Page("9OroBz49b9ycXw", ["AccountService.getAssetsForFeatureAndStatus"])],
    }

    eq_(classify(log_entries), expected)


def test_one_key_ordered():
    inputs = [
        TestObject(0, "auth1", "event0"),
        TestObject(1, "auth1", "event1"),
        TestObject(2, "auth1", "event2"),
    ]
    output = {
        "auth1": [
            Page("auth1", ["event0", "event1", "event2"]),
        ],
    }
    eq_(classify(inputs), output)


def test_one_key_unordered():
    inputs = [
        TestObject(1, "auth1", "event1"),
        TestObject(0, "auth1", "event0"),
        TestObject(2, "auth1", "event2"),
    ]
    output = {
        "auth1": [
            Page("auth1", ["event0", "event1", "event2"]),
        ],
    }
    eq_(classify(inputs), output)


def test_one_key_delta():
    """
    This function assume 3 seconds delta set in
    exemplar.classifier.group_by_time
    """
    inputs = [
        TestObject(0, "auth1", "event0"),
        TestObject(1, "auth1", "event1"),
        TestObject(10, "auth1", "event10"),
    ]
    output = {
        "auth1": [
            Page("auth1", ["event0", "event1"]),
            Page("auth1", ["event10"])
        ],
    }
    eq_(classify(inputs), output)


def test_two_keys_one_range():
    inputs = [
        TestObject(0, "auth1", "event0"),
        TestObject(1, "auth1", "event1"),
        TestObject(2, "auth1", "event2"),
        TestObject(0, "auth2", "event0"),
        TestObject(1, "auth2", "event1"),
        TestObject(2, "auth2", "event2"),
    ]
    output = {
        "auth1": [
            Page("auth1", ["event0", "event1", "event2"])
        ],
        "auth2": [
            Page("auth2", ["event0", "event1", "event2"])
        ]
    }

    eq_(classify(inputs), output)

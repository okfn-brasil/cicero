from collections import namedtuple

from cicero.models import Bill
from cicero.twitter import Twitter


Tweet = namedtuple("Tweet", ("id",))


def test_hashtags(bill):  # noqa
    twitter = Twitter()
    assert " ".join(twitter.hashtags) == "#Key #Word #KeyWord"


def test_publish(bill, mocker):
    api = mocker.patch("cicero.twitter.Api")
    api.return_value.PostUpdate.return_value = Tweet("42")
    twitter = Twitter()
    twitter.publish()
    expected = "PL 42 https://foob.ar/ #Key #Word #KeyWord"
    api.return_value.PostUpdate.assert_called_once_with(expected)
    assert Bill.get(Bill.id == bill.id).tweet == "42"

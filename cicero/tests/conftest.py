import pytest

from cicero import models
from cicero import settings
from cicero.items import Bill


@pytest.fixture(scope="function")
def db():
    models.create_tables()


@pytest.fixture
def item():
    return Bill(
        name="PL 42",
        keywords="key, word, key word",
        url="https://foob.ar/",
        source_id="42",
        created_at="2019-02-01",
    )


@pytest.fixture
def bill(db, item):
    bill = models.Bill.get_or_none(models.Bill.source_id == item["source_id"])
    return bill if bill else models.Bill.create(**dict(item))

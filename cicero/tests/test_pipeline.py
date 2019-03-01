from cicero.models import Bill
from cicero.pipelines import CiceroPipeline


def test_process_item(db, item):
    assert Bill.select().count() == 0
    pipeline = CiceroPipeline()

    # assert it saves item in the database
    pipeline.process_item(item, None)
    assert Bill.select().count() == 1

    # assert it does not duplicate items
    pipeline.process_item(item, None)
    assert Bill.select().count() == 1

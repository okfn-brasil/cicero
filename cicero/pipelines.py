from cicero.models import Bill


class CiceroPipeline:
    def process_item(self, item, spider):
        bill = Bill.get_or_none(Bill.source_id == int(item["source_id"]))
        if not bill:
            Bill.create(**dict(item))
        return item

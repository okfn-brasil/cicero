from scrapy import Field, Item


class Bill(Item):
    name = Field()
    created_at = Field()
    keywords = Field()
    url = Field()
    source_id = Field()

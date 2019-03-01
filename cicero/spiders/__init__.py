from scrapy import Spider

from cicero import settings
from cicero.strings import normalize


class BillSpider(Spider):

    def match(self, data, text):
        text = normalize(text)
        matches = (keyword for keyword in settings.KEYWORDS if keyword in text)
        data["keywords"] = data.get("keywords", set()) | set(matches)
        return data

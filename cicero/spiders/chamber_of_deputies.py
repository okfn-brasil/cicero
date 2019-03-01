import json
import re

from cicero import settings
from cicero.items import Bill
from cicero.requests import JsonRequest
from cicero.spiders import BillSpider


class ChamberOfDeputiesSpider(BillSpider):
    name = "chamber"
    subjects = ("PL", "PLS", "PEC")
    urls = {
        "list": (
            "https://dadosabertos.camara.leg.br/"
            "api/v2/proposicoes?siglaTipo={}&dataInicio={}&itens=100"
        ),
        "human": (
            "http://www.camara.gov.br/"
            "proposicoesWeb/fichadetramitacao?idProposicao={}"
        ),
    }

    def start_requests(self):
        subjects = ",".join(self.subjects)
        url = self.urls["list"].format(subjects, settings.START_DATE)
        yield JsonRequest(url, meta={"is_first": True})

    def parse(self, response):
        contents = json.loads(response.body_as_unicode())
        bills = contents.get("dados", tuple())
        for bill in bills:
            yield JsonRequest(bill.get("uri"), self.parse_bill)

        if "is_first" in response.meta:
            yield from self.request_all_remaining_pages(response)

    def request_all_remaining_pages(self, response):
        contents = json.loads(response.body_as_unicode())
        links = contents.get("links", tuple())
        pattern = r"pagina=(?P<last>\d+)"
        for link in links:
            if link.get("rel") == "last":
                url = link.get("href")
                match = re.search(pattern, url)
                last = int(match.group("last"))
                urls = (
                    re.sub(pattern, f"pagina={page}", url)
                    for page in range(2, last + 1)
                )
                return (JsonRequest(url) for url in urls)

    def parse_bill(self, response):
        bill = json.loads(response.body_as_unicode()).get("dados", {})
        data = {
            "keywords": set(),  # include matching keywords in this list
            "name": "{} {}".format(bill.get("siglaTipo"), bill.get("numero")),
            "source_id": bill.get("id"),
            "created_at": bill.get("dataApresentacao")[:10],  # 10 chars date
            "url": self.urls["human"].format(bill.get("id")),
        }

        data = self.match(data, bill.get("ementa", ""))
        data = self.match(data, bill.get("keywords", ""))
        data["keywords"] = ", ".join(data["keywords"])

        return Bill(data) if data["keywords"] else None

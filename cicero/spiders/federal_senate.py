from scrapy import Request

from cicero import settings
from cicero.items import Bill
from cicero.spiders import BillSpider


class FederalSenateSpider(BillSpider):
    name = "senate"
    subjects = ("PLS", "PLC", "PEC")
    urls = {
        "list": (
            "http://legis.senado.leg.br/dadosabertos/"
            "materia/pesquisa/lista?sigla={}&tramitando=S&dataInicioApresentacao={}"
        ),
        "detail": "http://legis.senado.leg.br/dadosabertos/materia/{}",
        "texts": "http://legis.senado.leg.br/dadosabertos/materia/textos/{}",
        "humans": (
            "https://www25.senado.leg.br/" "web/atividade/materias/-/materia/{}"
        ),
    }

    def start_requests(self):
        for subject in self.subjects:
            start_date = settings.START_DATE.replace("-", "")
            url = self.urls["list"].format(subject, start_date)
            yield Request(url=url)

    def parse(self, response):
        codes = response.xpath("//CodigoMateria/text()").extract()
        for code in codes:
            yield Request(
                url=self.urls["detail"].format(code),
                meta={"code": code},
                callback=self.parse_bill,
            )

    def parse_bill(self, response):
        description = response.xpath("//EmentaMateria/text()").extract_first()
        keywords = response.xpath("//IndexacaoMateria/text()").extract_first()
        number = response.xpath("//NumeroMateria/text()").extract_first()
        subject = response.xpath("//SiglaSubtipoMateria/text()").extract_first()

        data = {
            "keyword": set(),  # include matching keywords in this list
            "name": f"{subject} {number}",
            "source_id": response.xpath("//CodigoMateria/text()").extract_first(),
            "created_at": response.xpath("//DataApresentacao/text()").extract_first(),
            "url": self.urls["humans"].format(response.meta["code"]),
        }
        data = self.match(data, description)
        data = self.match(data, keywords)
        data["keywords"] = ", ".join(data["keywords"])

        return Bill(data) if data["keywords"] else None

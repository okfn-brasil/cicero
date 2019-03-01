from twitter import Api

from cicero import settings
from cicero.models import Bill


class Twitter:
    def __init__(self, mention=False):
        self.api = Api(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_SECRET,
        )
        self._bill = None

    @property
    def bill(self):
        if self._bill:
            return self._bill

        try:
            self._bill = (
                Bill.select()
                .where(Bill.tweet == "")
                .order_by(Bill.created_at.desc())
                .get()
            )
        except Bill.DoesNotExist:
            pass

        return self._bill

    @property
    def hashtags(self):
        for keyword in self.bill.keywords.split(","):
            words = "".join(w.capitalize() for w in keyword.strip().split(" "))
            yield f"#{words}"

    def publish(self):
        message = " ".join((self.bill.name, self.bill.url, " ".join(self.hashtags)))
        tweet = self.api.PostUpdate(message)
        self.bill.tweet = tweet.id
        self.bill.save()

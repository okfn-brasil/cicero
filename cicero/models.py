from sys import modules
from datetime import datetime

from peewee import (
    CharField,
    DateField,
    DateTimeField,
    IntegerField,
    Model,
    PostgresqlDatabase,
    SqliteDatabase,
)

from cicero import settings


def get_database():
    if "pytest" in modules:
        return SqliteDatabase(":memory:")

    return PostgresqlDatabase(
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )


class Bill(Model):
    name = CharField()
    created_at = DateField(index=True)
    keywords = CharField()
    url = CharField()
    source_id = IntegerField(unique=True, index=True)
    tweet = CharField(default="", index=True)
    crawled_at = DateTimeField(index=True, default=datetime.now)

    class Meta:
        database = get_database()


def create_tables():
    db = get_database()
    if db.is_closed():
        db.connect()
    db.create_tables((Bill,))

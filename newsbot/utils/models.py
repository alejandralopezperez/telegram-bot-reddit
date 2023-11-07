from peewee import SqliteDatabase, Model, PrimaryKeyField, CharField, IntegerField, DateTimeField


db = SqliteDatabase('newsbot/data/newsbot.db')


class BaseModel(Model):
    class Meta:
        database = db


class Source(BaseModel):
    person_id = PrimaryKeyField()
    fetch_from = CharField()


class Request(BaseModel):
    id = PrimaryKeyField()
    from_id = IntegerField(index=True)
    request_text = CharField()
    received_time = DateTimeField()


class Message(BaseModel):
    id = PrimaryKeyField()
    sent_to_id = IntegerField(index=True)
    sent_message = CharField()
    sent_time = DateTimeField()


def create_tables():
    db.connect()
    db.create_tables([Source, Request, Message], True)
    db.close()

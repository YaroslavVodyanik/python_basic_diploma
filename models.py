from peewee import *

db = SqliteDatabase('history.db')

class RequestHistory(Model):
    user_id = IntegerField()
    timestamp = DateTimeField()
    query_type = CharField()
    params = TextField()
    movie_title = CharField(null=True)
    description = TextField(null=True)
    rating = CharField(null=True)
    year = IntegerField(null=True)
    genre = CharField(null=True)
    age_rating = CharField(null=True)
    poster_url = CharField(null=True)

    class Meta:
        database = db

from peewee import *
from config import DATABASE

sqlite_db = SqliteDatabase(
    DATABASE,
    pragmas=(
        ('foreign_keys', 'on'),
    )
)


class Classification(Model):
    name = CharField(max_length=255, null=False, unique=True)
    parent = IntegerField(null=True)

    class Meta:
        database = sqlite_db


class Album(Model):
    name = CharField(max_length=255, default='')
    artist = CharField(max_length=63, default='')
    is_hot = BooleanField(default=False)
    classification = ManyToManyField(Classification, backref='albums')

    class Meta:
        database = sqlite_db


AlbumClassificationThrough = Album.classification.get_through_model()


def create_tables():
    if not (Album.table_exists() and Classification.table_exists()):
        sqlite_db.create_tables([Album, Classification, AlbumClassificationThrough])

import peewee
from loguru import logger


db = peewee.SqliteDatabase('users.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': 10000,
    'foreign_keys': 1
}
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    name = peewee.CharField()
    telegram_id = peewee.IntegerField()
    ready_state = peewee.CharField(null=True)
    state = peewee.CharField(null=True)
    keyboard = peewee.IntegerField(null=True)
    generate_story = peewee.BooleanField()
    generate_image = peewee.BooleanField()


db.connect()
with db:
    User.create_table()


@logger.catch
def create_user(name, chat_id):
    with db:
        user = User.select().where(User.name == name, User.telegram_id == chat_id)
        if not user.exists():
            User.create(
                name=name,
                telegram_id=chat_id,
                ready_state='ready',
                state='main',
                keyboard=0,
                generate_story=True,
                generate_image=False
            )
        return User.get(name=name, telegram_id=chat_id)

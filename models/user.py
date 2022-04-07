from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    uname = fields.CharField(max_length=20, unique=True)
    passwd = fields.TextField()

    def __str__(self):
        return self.uname

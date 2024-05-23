from tortoise.models import Model
from tortoise import fields


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100)
    posts = fields.ReverseRelation['Post']

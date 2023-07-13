from mongoengine import *

class UserDetails(Document):
	name = StringField(max_length=100)
	marks = IntField()
	gameNumber = StringField()
	randomNumber = IntField()
	createdOn = DateTimeField()
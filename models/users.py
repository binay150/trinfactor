from google.appengine.ext import db

class UserAccount(db.Model):
	User = db.StringProperty(required = True)
	Password = db.StringProperty(required = True)
	Email = db.StringProperty(required = False)

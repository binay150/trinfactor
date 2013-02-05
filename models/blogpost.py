from google.appengine.ext import db

class Blogpost(db.Model):
	bpost = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	user = db.StringProperty(required = True)


class Purchase_Order(db.Model):
	User = db.TextProperty(required=True)
	Address = db.TextProperty(required = True)
	City = db.TextProperty(required = True)
	State = db.TextProperty(required = True)
	Country = db.TextProperty(required = True)
	Quantity = db.TextProperty(required = True)
